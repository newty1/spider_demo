import xlwt
workbook =xlwt.Workbook(encoding="utf-8") # 创建workbook 对象
worksheet = workbook.add_sheet("sheet1") #  创建工作表
worksheet.write(0,0,'hello')# 写入数据 第一行参数行 第二个 列 第三个 内容
workbook.save('student.xls') # 保存数据表


