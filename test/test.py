import unittest
from strmprivacy.diagnostics import PrivacyDiagnostics


class MyTestCase(unittest.TestCase):
    d = PrivacyDiagnostics("datasets/simpleset.csv")

    def test_happy_flow_1qi_1sa(self):
        d = self.d
        d.calculate_stats(
            qi=['col3'],
            sa=['col1'],
        )
        self.assertEqual(4, min(d.k), "k-anonymity for 'col3' is incorrect")
        self.assertEqual(2, min(d.l['col1']), "l-diversity for 'col1' is incorrect")
        self.assertAlmostEqual(0.23333, d.t, 4)

    def test_happy_flow_2qi_1sa(self):
        d = self.d
        d.calculate_stats(
            qi=['col3', 'col4'],
            sa=['col1'],
        )
        self.assertEqual(2, min(d.k), "k-anonymity for ['col3', 'col4'] is incorrect")
        self.assertEqual(2, min(d.l['col1']), "l-diversity for 'col1' is incorrect")
        self.assertAlmostEqual(0.43333, d.t, 4)

    def test_happy_flow_1qi_2sa(self):
        d = self.d
        sa = ['col1', 'col2']
        d.calculate_stats(
            qi=['col4'],
            sa=sa
        )
        self.assertEqual(14, min(d.k), "k-anonymity for ['col3'] is incorrect")
        self.assertEqual(3, min(d.l['col1']), f"l-diversity for 'col1' is incorrect")
        self.assertEqual(14, min(d.l['col2']), f"l-diversity for 'col2' is incorrect")
        self.assertAlmostEqual(0.05238, d.t, 4)

    def test_non_existing_qi(self):
        d = self.d
        with self.assertRaises(AssertionError) as context:
            d.calculate_stats(
                qi=['non-existent'],
                sa=['col1']
            )
        self.assertIn(
            "Column 'non-existent' does not exist in the given dataset",
            str(context.exception)
        )

    def test_sa_types_not_matching_sa_len(self):
        d = self.d
        with self.assertRaises(AssertionError) as context:
            d.calculate_stats(
                qi=['non-existent'],
                sa=['col1', 'col2'],
                sa_types=['cat']
            )
        self.assertIn(
            "Length of sa-types doesn't equal length of sa. Either leave empty or set all data types explicitly.",
            str(context.exception)
        )

    def test_sa_types_not_valid(self):
        d = self.d
        with self.assertRaises(AssertionError) as context:
            d.calculate_stats(
                qi=['non-existent'],
                sa=['col1', 'col2'],
                sa_types=['bla', 'num']
            )
        self.assertIn(
            "Wrong type given for sensitive attribute. Valid types: [cat, num]",
            str(context.exception)
        )

    def test_empty_qi(self):
        d = self.d
        with self.assertRaises(AssertionError) as context:
            d.calculate_stats(
                qi=[],
                sa=['col1', 'col2'],
            )
        self.assertIn(
            "No quasi identifiers were defined. Please define at least one quasi identifier.",
            str(context.exception)
        )

    def test_empty_sa(self):
        d = self.d
        with self.assertRaises(AssertionError) as context:
            d.calculate_stats(
                qi=['col1'],
                sa=[],
            )
        self.assertIn(
            "No sensitive attributes were defined. Please define at least one sensitive attributes.",
            str(context.exception)
        )

    def test_unknown_metric(self):
        d = self.d
        with self.assertRaises(AssertionError) as context:
            d.calculate_stats(
                qi=['col1'],
                sa=['col2'],
                metrics=['non-existent']
            )
        self.assertIn(
            "Unknown metrics specified. Valid types: [k_anonymity, l_diversity, t_closeness]", str(context.exception)
        )


if __name__ == '__main__':
    unittest.main()
