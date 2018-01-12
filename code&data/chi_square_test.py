import xlrd
import numpy
from scipy.stats import chi2_contingency
from scipy.stats import fisher_exact

def conduct_test(element, pp, pn, np, nn):
    '''calculate chi-square test or fisher test'''
    min_value = min([pp, pn, np, nn])
    sum_value = sum([pp, pn, np, nn])
    print [[pp, pn], [np, nn]]
    if min_value>1 and min_value<5 and sum_value>=40:
        chi_result = chi2_contingency(numpy.array([[pp, pn],[np, nn]]).T)
        p_value = chi_result[1]
        if p_value < 0.05:
            print 'yes', element, chi_result
    elif min_value>=5 and sum_value>=40:
        chi_result = chi2_contingency(numpy.array([[pp, pn],[np, nn]]).T, correction=False)
        p_value = chi_result[1]
        if p_value < 0.05:
            print 'yes', element, chi_result
    elif sum_value<40:
        fisher_result = fisher_exact(numpy.array([[pp, pn],[np, nn]]).T)
        p_value = fisher_result[1]
        if p_value < 0.05:
            print 'yes', element, fisher_result
        
        
def count_datasets(table_data):
    '''conduct chi-square test or fisher exact test for all elements'''
    n_rows = table_data.nrows
    n_cols = table_data.ncols
    for c in range(2,n_cols):
        header_list = table_data.row_values(0)
        name = header_list[c]
        pp = float(0)
        pn = float(0)
        np = float(0)
        nn = float(0)
        for r in range(1,n_rows):
            if table_data.row_values(r)[c] == '+':
                if table_data.row_values(r)[1] == 1:
                    pp += 1
                elif table_data.row_values(r)[1] == 0:
                    np += 1
            if table_data.row_values(r)[c] == '-':
                if table_data.row_values(r)[1] == 1:
                    pn += 1
                elif table_data.row_values(r)[1] == 0:
                    nn += 1
        print name
        print conduct_test(name, pp, pn, np, nn)


def main():
    file_path = 'IHC features and tumor embolus.xlsx'
    bk = xlrd.open_workbook(file_path)
    n_sheets = bk.nsheets
    for i in range(n_sheets):
        table = bk.sheet_by_index(i)
        count_datasets(table)
if __name__ == '__main__':
    main()
