import xlrd

if __name__ == "__main__":

    data = xlrd.open_workbook('./情感词汇本体.xls')
    sh = data.sheet_by_name('Sheet1')
    with open('positive_word.txt','w',encoding='UTF-8')as f1:
        with open('negative_word.txt','w',encoding='UTF-8')as f2:
            for i in range(1,sh.nrows):  # 0代表中性，1代表褒义，2代表贬义，3代表兼有褒贬两性。
                if int(sh.cell_value(i, 6)) == 1:
                    f1.write(sh.cell_value(i, 0))
                    f1.write('\n')
                elif int(sh.cell_value(i, 6)) == 2:
                    f2.write(sh.cell_value(i, 0))
                    f2.write('\n')
