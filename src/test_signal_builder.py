import sys
from pathlib import Path
import uuid
import unittest
import csv
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from signal_builder import BuildSignal, SignalBuilder, BuildSumWave, BuildLinearWave, BuildProductWave
from signal_parser import SignalParser

class SignalBuildTests(unittest.TestCase):
    def test_known_pair_and_alignment(self):
        s = BuildSignal('א ב\nת')
        self.assertEqual(s.base,(1,2,400))
        self.assertEqual(s.source_indices,(0,2,4))
        self.assertEqual((s.sum_wave,s.linear_wave,s.product_wave),((3,171),(24,213),(2,107)))
        self.assertEqual(list(s.rows())[-1],(2,4,400,None,None,None,None,None))
        folder = Path(__file__).resolve().parents[1]/'research/Tanakh/signal_waves_v1'
        with self.subTest('CSV export'):
            path = s.SaveCSV(Path(folder)/('test_'+uuid.uuid4().hex+'.csv'))
            with path.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
            self.assertEqual(rows[-1]['sum_wave'],'')
            with self.assertRaises(FileExistsError): s.SaveCSV(path)

    def test_agrees_with_existing_parser(self):
        text='דבריעםוסאש ךםןףץ'
        triples=SignalParser().derive_checksum_triples(text)
        s=SignalBuilder().BuildSignal(text)
        self.assertEqual(s.sum_wave,tuple(t['sum'] for t in triples))
        self.assertEqual(s.linear_wave,tuple(t['linear'] for t in triples))
        self.assertEqual(s.product_wave,tuple(t['product'] for t in triples))
        self.assertEqual(s.source_indices,tuple(SignalParser().parse_hebrew(text)['mapped_indices']))

    def test_empty_single_and_exact_large_integers(self):
        self.assertEqual(list(BuildSignal([]).rows()),[])
        self.assertEqual(BuildSignal([0]).sum_wave,())
        large=10**40+7
        self.assertEqual(BuildSignal([large,2]).linear_wave,((large*22+2)%231,))
        self.assertEqual(BuildSignal('ךםןףץ').base,(20,40,50,80,90))

    def test_parameters_and_errors(self):
        self.assertEqual(BuildSignal([2,3],modulus=7,multiplier=4).linear_wave,(4,))
        self.assertEqual(SignalBuilder({'hebrew':{'א':9}}).BuildSignal('אב').base,(9,2))
        with self.assertRaises(ValueError): BuildSignal('א ',rules={'unknown':'error'})
        for bad in (0,-1,True,2.5):
            with self.assertRaises(ValueError): BuildSumWave([1,2],bad)
        for bad in ([True,1],[1.5,2]):
            with self.assertRaises(TypeError): BuildProductWave(bad)
        with self.assertRaises(TypeError): BuildLinearWave([1,2],multiplier=1.5)

if __name__=='__main__': unittest.main()
