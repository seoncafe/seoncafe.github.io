#!/usr/bin/env python3
"""Render managed courses into Teaching.html using only Python's standard library."""
import argparse
import csv
import hashlib
import html
import io
import json
import subprocess
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['lecture', 'date', 'time', 'title', 'pdf', 'updated']
START = '<!-- BEGIN MANAGED COURSES -->'
END = '<!-- END MANAGED COURSES -->'


def csv_text(rows):
    output = io.StringIO(newline='')
    writer = csv.DictWriter(output, fieldnames=FIELDS, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def valid_date(value):
    if value:
        date.fromisoformat(value)
    return value


def escape(value):
    return html.escape(str(value), quote=True)


def render_course(course, rows, folder, root, hashes):
    lines = ['<section class="managed-course">', '<hr class="course-divider">',
             f'<h2 class="p17 f112">&lt; {escape(course["title"])} ({escape(course["term"])}) &gt;</h2>',
             '<h3 class="p19 f113">Date &amp; Time</h3>',
             f'<p class="p20 f114">{escape(course["schedule"])}</p>']
    if course.get('references'):
        lines.append('<h3 class="p19 f113">References</h3>')
        for ref in course['references']:
            label = escape(ref['title'])
            if ref.get('url'):
                label = f'<a class="f122" href="{escape(ref["url"])}">{label}</a>'
            lines.append(f'<p class="p20 f115">{label}</p>')
    lines.append('<h3 class="p20 f116">Lecture Notes</h3>')
    for row in rows:
        label = f'Lecture {int(row["lecture"]):02d}'
        pdf = folder / row['pdf'] if row['pdf'] else None
        if pdf and pdf.is_file():
            href = quote(pdf.resolve().relative_to(root.resolve()).as_posix(), safe='/')
            label = f'<a class="f118" href="{href}?v={hashes[row["pdf"]][:12]}">{label}</a>'
        else:
            label = f'<span class="lecture-pending">{label}</span>'
        when = date.fromisoformat(row['date']).strftime('%m/%d') if row['date'] else 'TBA'
        if row['time']:
            hour, minute = map(int, row['time'].split(':'))
            when += f', {hour % 12 or 12}' + (f':{minute:02d}' if minute else '') + ('AM' if hour < 12 else 'PM')
        updated = date.fromisoformat(row['updated']).strftime('%m/%d') if row['updated'] else '—'
        lines.append(f'<p class="p20 f117">&bull; {label} <span class="f119">({when}) : '
                     f'{escape(row["title"])} [update: {updated}]</span></p>')
    lines.append('</section>')
    return '\n'.join(lines)


def update(root=ROOT):
    target = root / 'Teaching.html'
    page = target.read_text(encoding='utf-8')
    if page.count(START) != 1 or page.count(END) != 1:
        raise ValueError('Teaching.html: managed-course markers are missing or duplicated')
    pending, courses, messages = [], [], []
    for config in sorted((root / 'Teaching_files').glob('*/course.json')):
        folder = config.parent
        course = json.loads(config.read_text(encoding='utf-8'))
        for key in ['title', 'term', 'schedule', 'sort_date']:
            if not isinstance(course.get(key), str) or not course[key].strip():
                raise ValueError(f'{config}: {key} is required')
        valid_date(course['sort_date'])
        for ref in course.get('references', []):
            if not ref.get('title') or (ref.get('url') and not ref['url'].startswith(('https://', 'http://'))):
                raise ValueError(f'{config}: invalid reference title/URL')
        source = folder / 'lectures.csv'
        with source.open(encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != FIELDS:
                raise ValueError(f'{source}: columns must be {FIELDS}')
            rows = []
            for row in reader:
                if None in row or any(value is None for value in row.values()):
                    count = (len(FIELDS) + len(row.get(None, []))
                             - sum(value is None for value in row.values()))
                    raise ValueError(
                        f'{source}:{reader.line_num}: incorrect CSV field count '
                        f'(expected {len(FIELDS)}, got {count}). '
                        'Wrap fields containing commas in double quotes.'
                    )
                rows.append(row)
        state_path = folder / '.pdf-hashes.json'
        state, numbers = {}, set()
        for row in rows:
            number = int(row['lecture'])
            if number < 1 or number in numbers or not row['title'].strip():
                raise ValueError(f'{source}: duplicate/invalid lecture number or empty title')
            numbers.add(number)
            valid_date(row['date']); valid_date(row['updated'])
            if row['time']:
                datetime.strptime(row['time'], '%H:%M')
            pdf = (folder / row['pdf']).resolve() if row['pdf'] else None
            if pdf and (not pdf.is_relative_to(root.resolve() / 'Teaching_files') or pdf.suffix.lower() != '.pdf'):
                raise ValueError(f'{source}: PDF must be inside Teaching_files: {row["pdf"]}')
            digest = hashlib.sha256(pdf.read_bytes()).hexdigest() if pdf and pdf.is_file() else None
            if row['pdf']:
                state[row['pdf']] = digest
            if digest:
                modified = datetime.fromtimestamp(pdf.stat().st_mtime, ZoneInfo('Asia/Seoul')).date().isoformat()
                if row['updated'] != modified:
                    row['updated'] = modified
                    messages.append(f'{folder.name}: Lecture {number:02d} updated {modified} (PDF modified date)')
            if not digest:
                messages.append(f'{folder.name}: Lecture {number:02d} PDF pending (shown without a link)')
        rows.sort(key=lambda row: int(row['lecture']))
        pending.extend([(source, csv_text(rows)), (state_path, json_text(state))])
        courses.append((course['sort_date'], folder.name, render_course(course, rows, folder, root, state)))
    if not courses:
        raise ValueError('No Teaching_files/*/course.json found')
    content = '\n'.join(c[2] for c in sorted(courses, reverse=True))
    before, rest = page.split(START)
    _, after = rest.split(END)
    pending.append((target, before + START + '\n' + content + '\n' + END + after))
    # Validate every course before writing any output.
    changed = []
    for path, text in pending:
        if not path.exists() or path.read_text(encoding='utf-8') != text:
            path.write_text(text, encoding='utf-8')
            changed.append(path.relative_to(root).as_posix())
    return changed, messages


def new_course(root, slug, title, term, schedule, sort_date):
    if not slug or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in slug):
        raise ValueError('Course folder name may contain only letters, digits, _ and -')
    valid_date(sort_date)
    folder = root / 'Teaching_files' / slug
    if (folder / 'course.json').exists() or (folder / 'lectures.csv').exists():
        raise ValueError(f'{folder}: course files already exist')
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'course.json').write_text(json_text(dict(title=title, term=term, schedule=schedule,
                                                       sort_date=sort_date, references=[])), encoding='utf-8')
    (folder / 'lectures.csv').write_text(csv_text([dict(lecture='1', date='', time='', title='Introduction',
                                                        pdf='lecture01.pdf', updated='')]), encoding='utf-8')


def publish(root=ROOT, message='Update lecture notes and teaching schedule'):
    """Commit managed teaching files and push the current branch to origin."""
    def git(*args):
        result = subprocess.run(['git', *args], cwd=root, text=True, capture_output=True)
        if result.returncode:
            raise ValueError(f'git {args[0]} failed: {result.stderr.strip() or result.stdout.strip()}')
        return result.stdout.strip()

    branch = git('symbolic-ref', '--short', 'HEAD')
    git('remote', 'get-url', 'origin')
    paths = {'Teaching.html'}
    for config in (root / 'Teaching_files').glob('*/course.json'):
        folder = config.parent
        paths.update((folder / name).relative_to(root).as_posix()
                     for name in ['course.json', 'lectures.csv', '.pdf-hashes.json'])
        with (folder / 'lectures.csv').open(encoding='utf-8-sig', newline='') as stream:
            for row in csv.DictReader(stream):
                if row['pdf']:
                    paths.add((folder / row['pdf']).resolve().relative_to(root.resolve()).as_posix())
    tracked = set(git('ls-files', '-z', '--', *sorted(paths)).split('\0'))
    paths = sorted(path for path in paths if (root / path).exists() or path in tracked)
    git('add', '-A', '--', *paths)
    if git('diff', '--cached', '--name-only', '--', *paths):
        # --only preserves unrelated staged changes and excludes them from this commit.
        print(git('commit', '--only', '-m', message, '--', *paths))
    else:
        print('No teaching changes to commit; pushing any pending commits.')
    print(git('push', 'origin', f'HEAD:refs/heads/{branch}'))
    print(f'Pushed to origin/{branch}. GitHub Pages will update after deployment.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--new-course', metavar='FOLDER', help='Create course metadata and CSV; then regenerate the page')
    parser.add_argument('--title')
    parser.add_argument('--term', help='e.g. Spring, 2027')
    parser.add_argument('--schedule')
    parser.add_argument('--sort-date', help='Semester start, YYYY-MM-DD; newest course first')
    parser.add_argument('--publish', action='store_true', help='After updating, commit teaching files and push to origin')
    parser.add_argument('--message', default='Update lecture notes and teaching schedule', help='Commit message for --publish')
    args = parser.parse_args()
    try:
        if args.new_course:
            if not all([args.title, args.term, args.schedule, args.sort_date]):
                parser.error('--new-course requires --title, --term, --schedule, --sort-date')
            new_course(ROOT, args.new_course, args.title, args.term, args.schedule, args.sort_date)
        changed, messages = update()
        for message in messages:
            print(message)
        print('Changed: ' + ', '.join(changed) if changed else 'No changes.')
        if args.publish:
            publish(message=args.message)
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    main()
