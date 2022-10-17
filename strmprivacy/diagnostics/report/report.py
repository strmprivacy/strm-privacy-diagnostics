import logging
from pathlib import Path

from fpdf import FPDF


class Report(FPDF):
    def __init__(self, orientation='P', unit='mm', format='A4', tmpdir=""):
        super().__init__(orientation, unit, format)
        self.tmpdir = tmpdir

    def header(self):
        # Arial bold 15
        try:
            self.set_font('Inter', size=15)
        except:
            self.set_font('arial', size=15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'STRM Privacy Report', 0, 0, 'C')
        # Line break
        self.ln(20)

    def intro(self):
        try:
            self.set_font('Inter', style="i", size=10)
        except:
            self.set_font('arial', style="i", size=10)
        self.write(h=5, txt=f"Using this report, you can assess if your privacy transformations are fit-for-purpose."
                            " K-anonymity, and l-diversity are methods to assess the degree of anonymity in a given dataset. T-closeness indicates the information loss in your data, and so its utility."
                            " The methods look at how unique a combination of datapoints is, giving you insight into the risk of re-identification: the less unique, the lower the probability you can find a single individual in the data."
                            " Therefore, generally speaking, higher scores are better: they indicate it's harder to find a single individual in your data."
                   )
        self.ln(5)

    def summation(self, k, l, t):
        try:
            self.set_font('Inter', size=8)
        except:
            self.set_font('arial', size=8)

        i = 1
        if k is not None:
            self.write(h=5, txt=f"{i}. Your data has a k-Anonymity of {min(k)}")
            self.ln(5)
            i += 1
        if l is not None:
            self.write(h=5, txt=f"{i}.  l-Diversity minimal distinct values per equivalence group: " +
                                ', '.join([f"{key}: {min(value)}" for key, value in l.items()]))
            self.ln(5)
            i += 1
        if t is not None:
            self.write(h=5, txt=f"{i}. Your data has a t-Closeness of {t:.4f}")
            self.ln(5)

    def plots(self, metric):
        width = self.w * 0.7
        height = width * 2 / 3
        x = (self.w - width) // 2
        y = self.y
        if y + height > self.h:
            self.add_page()
        self.image(str(Path(self.tmpdir, f'{metric}.png')), x=x, w=width, h=height)

    def k_metrics(self, k):
        try:
            self.set_font('Inter', size=12)
        except:
            self.set_font('arial', size=12)
        self.write(h=5, txt="k-Anonymity")
        self.ln(5)
        try:
            self.set_font('Inter', size=8)
        except:
            self.set_font('arial', size=8)
        self.write(h=5, txt=f'Your data has a k-Anonymity of  {min(k)}')
        self.ln(10)
        self.write(
            h=5,
            txt="K-anonymity indicates if you can isolate a given data subject, based on how many equal groups can be found in the data. "
                "Any K of or above 2 indicates at least two indivduals belong to any group inside the data."
                "The graph below should be read as follows. The unique rows line (blue) indicates what percentage of "
                "the total rows (y-axis) you will lose to achieve every k-Anonymity level (x-axis), "
                "without transforming data. The loss in unique equivalence groups line (orange) indicates the "
                "percentage of unique combinations of the values in the quasi identifier columns (y-axis) you will "
                "lose to achieve every k-Anonymity level (x-axis)."
        )
        self.ln(10)
        self.plots('k-Anonymity')
        self.ln(15)

    def l_metrics(self, l):
        try:
            self.set_font('Inter', size=12)
        except:
            self.set_font('arial', size=12)
        self.write(h=5, txt="l-Diversity")
        self.ln(5)
        try:
            self.set_font('Inter', size=8)
        except:
            self.set_font('arial', size=8)
        self.write(h=5, txt="Minimal distinct values per equivalence group:")
        self.ln(5)
        for k, v in l.items():
            self.write(h=5, txt=f'{k}: {min(v)}')
            self.ln(5)
        self.ln(5)
        self.write(
            h=5,
            txt="L-diversity extends k-anonymity by also looking at every attribute in each equivalence class (the group of equal attributes in your data). "
                "A higher L indicates higher variability in each class, so that attempts for re-identification always yield sufficient uncertainty on the exact individual within that class. "
                "The graphs below should be read as follows. The unique rows line (blue) indicates what percentage of "
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
        try:
            self.set_font('Inter', size=12)
        except:
            self.set_font('arial', size=12)
        self.write(h=5, txt="t-Closeness")
        self.ln(5)
        try:
            self.set_font('Inter', size=8)
        except:
            self.set_font('arial', size=8)
        self.write(h=5,
                   txt="T-closeness indicates how close the data in each L-diverse group is to the original data, and so how much utility is retained inside the data. "
                       " A T closer to 1 indicates the data is (statistically) closer to the input data.")
        self.ln(5)
        self.write(h=5, txt=f"Your data has a t-closeness of  {t:.4f}")
        self.ln(15)

    def create(self, k, l, t, path='.'):
        try:
            self.add_font('Inter', fname='strmprivacy/diagnostics/report/Inter-V.ttf', uni=True)
        except RuntimeError:
            logging.info('Inter not found, using arial')
        finally:
            self.accept_page_break()
            self.add_page()
            self.summation(k, l, t)
            if k is not None:
                self.k_metrics(k)
            if l is not None:
                self.l_metrics(l)
            if t is not None:
                self.t_metrics(t)
            Path(path, 'report.py')
            file_path = Path(path, 'STRM-Privacy-report.pdf')
            self.output(str(file_path), 'F')
            print(f"Report saved to {file_path}")
