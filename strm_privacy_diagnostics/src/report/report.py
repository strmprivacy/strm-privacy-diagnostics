from pathlib import Path

from fpdf import FPDF


class Report(FPDF):
    def __init__(self, orientation='P', unit='mm', format='A4', tmpdir=""):
        super().__init__(orientation, unit, format)
        self.tmpdir = tmpdir

    def header(self):
        # Arial bold 15
        self.set_font('Inter', size=15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'STRM Privacy Report', 0, 0, 'C')
        # Line break
        self.ln(20)

    def plots(self, metric):
        width = self.w * 0.7
        height = width * 2 / 3
        self.image(str(Path(self.tmpdir, f'{metric}.png')), w=width, h=height)

    def k_metrics(self, k):
        self.set_font('Inter', size=12)
        self.write(h=5, txt="k-Anonymity")
        self.ln(5)
        self.set_font('Inter', size=8)
        self.write(h=5, txt=f'Your data has a k-Anonymity of {min(k)}')
        self.ln(10)
        self.write(
            h=5,
            txt="The graph below should be read as follows. The unique rows line (blue) indicates what percentage of "
                "the total rows (y-axis) you will lose to achieve every k-Anonymity level (x-axis), "
                "without transforming data. The loss in unique equivalence groups line (orange) indicates the "
                "percentage of unique combinations of the values in the quasi identifier columns (y-axis) you will "
                "lose to achieve every k-Anonymity level (x-axis)."
        )
        self.ln(10)
        self.plots('k-Anonymity')
        self.ln(15)

    def l_metrics(self, l):
        self.set_font('Inter', size=12)
        self.write(h=5, txt="l-Diversity")
        self.ln(5)
        self.set_font('Inter', size=8)
        self.write(h=5, txt="Minimal distinct values per equivalence group:")
        self.ln(5)
        for k, v in l.items():
            self.write(h=5, txt=f'{k}: {min(v)}')
            self.ln(5)
        self.ln(5)
        self.write(
            h=5,
            txt="The graphs below should be read as follows. The unique rows line (blue) indicates what percentage of "
                "the total rows (y-axis) you will lose to achieve every l-Diversity level (x-axis) for each sensitive "
                "attribute individually. The loss in unique equivalence groups line (orange) indicates the percentage "
                "of unique combinations of the values in the quasi identifier columns (y-axis) you will lose to "
                "achieve every l-Diversity level (x-axis) for each sensitive attribute. "
        )
        self.ln(10)
        for k, v in l.items():
            self.plots(f'l-Diversity ({k})')
            self.ln(10)

    def t_metrics(self, t):
        self.set_font('Inter', size=12)
        self.write(h=5, txt="t-Closeness")
        self.ln(5)
        self.set_font('Inter', size=8)
        self.write(h=5, txt=f"Your data has a t-closeness of: {t:.4f}")
        self.ln(15)

    def create(self, k, l, t, path='.'):
        self.add_font('Inter', fname='report/Inter-V.ttf', uni=True)
        self.accept_page_break()
        self.add_page()
        if k is not None:
            self.k_metrics(k)
        if l is not None:
            self.l_metrics(l)
        if t is not None:
            self.t_metrics(t)
        Path(path, 'report.py')
        self.output(str(Path(path, 'report.pdf')), 'F')
        print(f"Report saved to {Path(path, 'report.pdf')}")
