import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT=Path(__file__).resolve().parents[1]/'skills/chaptr/scripts/chaptr.py'
spec=importlib.util.spec_from_file_location('chaptr',SCRIPT)
chaptr=importlib.util.module_from_spec(spec);spec.loader.exec_module(chaptr)

class SubtitleTests(unittest.TestCase):
    def test_parse(self):
        raw=b'1\n00:00:00,000 --> 00:00:02,000\nHello\n\n2\n00:00:02,000 --> 00:00:04,000\nWorld\n'
        rows=chaptr.parse_srt(raw)
        self.assertEqual(len(rows),2)
        self.assertEqual(rows[1]['startMs'],2000)
        self.assertEqual(rows[0]['id'],'cue-000001')
    def test_bad_clock(self):
        with self.assertRaises(ValueError):
            chaptr.srt_time('00:77:01,000')
    def test_empty_srt(self):
        with self.assertRaises(ValueError):
            chaptr.parse_srt(b'')
if __name__=='__main__':unittest.main()
