import pickle
fyear_line1 = 'fiscal year ended December 31, 2005'
fyear_line2 = 'fiscal year ended December 31, 2010'
fyear_line3 = 'fiscal year ended December 31, 1995'
fyear_line4 = 'fiscal year ended 12/03/97'
fyear_line5 = 'fiscal year ended 12/03/1997'
fyear_line6 = 'fiscal year ended 12/03/2010'
fyear_line6 = 'fiscal year ended 12/03/10'
fyear_line7 = 'fiscal year ended 12-31-2005'
fyear_line8 = 'fiscal year ended 12-31-05'
fyear_line9 = 'fiscal year ended 12-31-1995'
fyear_line10 = 'fiscal year ended 12-31-95'
fyear_line11 = 'fiscal year ended 12-2005'
fyear_line12 = 'fiscal year ended 12-1995'
fyear_test_lines = [fyear_line1, fyear_line2, fyear_line3,
               fyear_line4, fyear_line5, fyear_line6,
               fyear_line7, fyear_line8, fyear_line9,
               fyear_line10, fyear_line11, fyear_line12]
pickle.dump(fyear_test_lines, open('fiscal-year-tests.txt','w'))
