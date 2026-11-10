import csv
import importlib.util
import os
import subprocess
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('teaching', Path(__file__).resolve().parents[1] / 'scripts/update_teaching.py')
teaching = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(teaching)


class TeachingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'Teaching.html').write_text('HEADER\n' + teaching.START + '\n' + teaching.END + '\nARCHIVE')
        teaching.new_course(self.root, '2027a_Test', 'Test & <Course>', 'Spring, 2027', 'Monday / Room 1', '2027-03-01')
        self.folder = self.root / 'Teaching_files/2027a_Test'

    def rows(self):
        with (self.folder / 'lectures.csv').open(newline='') as stream:
            return list(csv.DictReader(stream))

    def write_rows(self, rows):
        (self.folder / 'lectures.csv').write_text(teaching.csv_text(rows))

    def set_mtime(self, pdf, timestamp):
        stamp = datetime.fromisoformat(timestamp).timestamp()
        os.utime(pdf, (stamp, stamp))

    def test_pdf_mtime_overrides_csv_and_same_day_cache(self):
        pdf = self.folder / 'lecture01.pdf'
        pdf.write_bytes(b'%PDF original')
        self.set_mtime(self.folder / 'lecture01.pdf', '2027-03-01T12:00:00+09:00')
        teaching.update(self.root)
        self.assertEqual(self.rows()[0]['updated'], '2027-03-01')
        first = (self.root / 'Teaching.html').read_text()
        self.assertIn('Test &amp; &lt;Course&gt;', first)
        self.assertEqual(teaching.update(self.root)[0], [])
        self.set_mtime(pdf, '2027-03-02T12:00:00+09:00')
        teaching.update(self.root)
        self.assertEqual(self.rows()[0]['updated'], '2027-03-02')
        pdf.write_bytes(b'%PDF replaced')
        self.set_mtime(pdf, '2027-03-02T13:00:00+09:00')
        teaching.update(self.root)
        second = (self.root / 'Teaching.html').read_text()
        self.assertEqual(self.rows()[0]['updated'], '2027-03-02')
        pdf.write_bytes(b'%PDF replaced again on same day')
        self.set_mtime(pdf, '2027-03-02T14:00:00+09:00')
        teaching.update(self.root)
        self.assertNotEqual(second, (self.root / 'Teaching.html').read_text())

    def test_pending_pdf_becomes_link_and_shared_pdf_updates_both(self):
        rows = self.rows()
        rows.append(dict(rows[0], lecture='2', title='Second lecture'))
        self.write_rows(rows)
        teaching.update(self.root)
        self.assertNotIn('<a ', (self.root / 'Teaching.html').read_text())
        (self.folder / 'lecture01.pdf').write_bytes(b'%PDF shared')
        self.set_mtime(self.folder / 'lecture01.pdf', '2027-03-02T12:00:00+09:00')
        teaching.update(self.root)
        self.assertTrue(all(r['updated'] == '2027-03-02' for r in self.rows()))
        self.assertEqual((self.root / 'Teaching.html').read_text().count('<a '), 2)

    def test_utc_timestamp_uses_korea_date_and_older_mtime(self):
        pdf = self.folder / 'lecture01.pdf'
        pdf.write_bytes(b'%PDF historical')
        self.set_mtime(pdf, '2026-10-18T16:00:00+00:00')
        rows = self.rows(); rows[0]['updated'] = '2027-12-31'; self.write_rows(rows)
        teaching.update(self.root)
        self.assertEqual(self.rows()[0]['updated'], '2026-10-19')
        self.assertIn('[update: 10/19]', (self.root / 'Teaching.html').read_text())
        self.assertEqual(teaching.update(self.root)[0], [])

    def test_publish_commits_notes_preserves_unrelated_staged_and_retries_push(self):
        def git(*args):
            return subprocess.run(['git', *args], cwd=self.root, check=True,
                                  text=True, capture_output=True).stdout.strip()
        remote = self.root / 'remote.git'
        subprocess.run(['git', 'init', '--bare', str(remote)], check=True, capture_output=True)
        git('init', '-b', 'master')
        git('config', 'user.name', 'Test')
        git('config', 'user.email', 'test@example.com')
        git('remote', 'add', 'origin', str(remote))
        git('add', 'Teaching.html'); git('commit', '-m', 'Initial')
        unrelated = self.root / 'unrelated.txt'
        unrelated.write_text('Leave staged')
        git('add', 'unrelated.txt')
        (self.folder / 'lecture01.pdf').write_bytes(b'%PDF publish')
        teaching.update(self.root)
        teaching.publish(self.root)
        files = git('show', '--pretty=', '--name-only', 'HEAD')
        self.assertIn('Teaching.html', files)
        self.assertIn('Teaching_files/2027a_Test/lecture01.pdf', files)
        self.assertIn('Teaching_files/2027a_Test/lectures.csv', files)
        self.assertNotIn('unrelated.txt', files)
        self.assertEqual(git('diff', '--cached', '--name-only'), 'unrelated.txt')
        head = git('rev-parse', 'HEAD')
        teaching.publish(self.root)
        self.assertEqual(git('rev-parse', 'HEAD'), head)
        self.assertEqual(git('rev-parse', 'origin/master'), head)

    def test_course_order_and_archive_preservation(self):
        teaching.new_course(self.root, '2027b_New', 'Newest', 'Fall, 2027', 'TBA', '2027-09-01')
        teaching.update(self.root)
        page = (self.root / 'Teaching.html').read_text()
        self.assertLess(page.index('Newest'), page.index('Test &amp;'))
        self.assertTrue(page.startswith('HEADER\n'))
        self.assertTrue(page.endswith('\nARCHIVE'))

    def test_invalid_csv_changes_no_files(self):
        teaching.update(self.root)
        rows = self.rows(); rows[0]['date'] = '2027-02-30'; self.write_rows(rows)
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with self.assertRaises(ValueError):
            teaching.update(self.root)
        self.assertTrue(all(p.read_bytes() == data for p, data in before.items()))

    def test_quoted_title_with_commas_and_newline(self):
        rows = self.rows()
        rows[0]['title'] = 'Clouds, Hazes,\nand Scattering'
        self.write_rows(rows)
        teaching.update(self.root)
        self.assertEqual(self.rows()[0]['title'], rows[0]['title'])
        self.assertIn(rows[0]['title'], (self.root / 'Teaching.html').read_text())

    def test_csv_field_count_reports_line_and_changes_no_files(self):
        cases = [
            ('1,,,Clouds, Hazes, and Scattering,lecture01.pdf,', 8),
            ('1,,,Introduction,lecture01.pdf', 5),
        ]
        for record, count in cases:
            with self.subTest(count=count):
                (self.folder / 'lectures.csv').write_text(
                    ','.join(teaching.FIELDS) + '\n' + record + '\n')
                before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
                with self.assertRaises(ValueError) as error:
                    teaching.update(self.root)
                self.assertIn(f'lectures.csv:2: incorrect CSV field count (expected 6, got {count})',
                              str(error.exception))
                self.assertIn('double quotes', str(error.exception))
                self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_rename_stamps_date_and_duplicate_number_rejected(self):
        (self.folder / 'lecture01.pdf').write_bytes(b'%PDF original')
        teaching.update(self.root)
        (self.folder / 'renamed.pdf').write_bytes(b'%PDF new name')
        rows = self.rows(); rows[0]['pdf'] = 'renamed.pdf'; self.write_rows(rows)
        self.set_mtime(self.folder / 'renamed.pdf', '2027-03-02T12:00:00+09:00')
        teaching.update(self.root)
        self.assertEqual(self.rows()[0]['updated'], '2027-03-02')
        rows = self.rows(); self.write_rows(rows + rows)
        with self.assertRaises(ValueError):
            teaching.update(self.root)


if __name__ == '__main__':
    unittest.main()
