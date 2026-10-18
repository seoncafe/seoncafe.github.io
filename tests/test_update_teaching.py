import csv
import importlib.util
import json
import tempfile
import unittest
from datetime import date
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

    def test_new_pdf_replacement_unchanged_copy_and_same_day_cache(self):
        pdf = self.folder / 'lecture01.pdf'
        pdf.write_bytes(b'%PDF original')
        teaching.update(self.root, date(2027, 3, 1))
        self.assertEqual(self.rows()[0]['updated'], '2027-03-01')
        first = (self.root / 'Teaching.html').read_text()
        self.assertIn('Test &amp; &lt;Course&gt;', first)
        pdf.touch()
        self.assertEqual(teaching.update(self.root, date(2027, 3, 2))[0], [])
        pdf.write_bytes(b'%PDF replaced')
        teaching.update(self.root, date(2027, 3, 2))
        second = (self.root / 'Teaching.html').read_text()
        self.assertEqual(self.rows()[0]['updated'], '2027-03-02')
        pdf.write_bytes(b'%PDF replaced again on same day')
        teaching.update(self.root, date(2027, 3, 2))
        self.assertNotEqual(second, (self.root / 'Teaching.html').read_text())

    def test_pending_pdf_becomes_link_and_shared_pdf_updates_both(self):
        rows = self.rows()
        rows.append(dict(rows[0], lecture='2', title='Second lecture'))
        self.write_rows(rows)
        teaching.update(self.root, date(2027, 3, 1))
        self.assertNotIn('<a ', (self.root / 'Teaching.html').read_text())
        (self.folder / 'lecture01.pdf').write_bytes(b'%PDF shared')
        teaching.update(self.root, date(2027, 3, 2))
        self.assertTrue(all(r['updated'] == '2027-03-02' for r in self.rows()))
        self.assertEqual((self.root / 'Teaching.html').read_text().count('<a '), 2)

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

    def test_rename_stamps_date_and_duplicate_number_rejected(self):
        (self.folder / 'lecture01.pdf').write_bytes(b'%PDF original')
        teaching.update(self.root, date(2027, 3, 1))
        (self.folder / 'renamed.pdf').write_bytes(b'%PDF new name')
        rows = self.rows(); rows[0]['pdf'] = 'renamed.pdf'; self.write_rows(rows)
        teaching.update(self.root, date(2027, 3, 2))
        self.assertEqual(self.rows()[0]['updated'], '2027-03-02')
        rows = self.rows(); self.write_rows(rows + rows)
        with self.assertRaises(ValueError):
            teaching.update(self.root)


if __name__ == '__main__':
    unittest.main()
