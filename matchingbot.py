#!/usr/bin/env python3
import gspread
from oauth2client.service_account import ServiceAccountCredentials 

SPREADSHEET_KEY = ''
key_file = ''
row_from, row_to = 4, 500

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file, scope)
gc = gspread.authorize(credentials)
workbook = gc.open_by_key(SPREADSHEET_KEY)
worksheet = workbook.sheet1

cells = worksheet.get('A{}:D{}'.format(row_from, row_to))
agreements = []
N = len(cells)
for i in range(N):
    if len(cells[i]) != 3:
        continue
    ci, hsi = cells[i][1:3]
    for h in hsi:
        for j in range(i+1,N):
            if len(cells[j]) != 3:
                continue
            cj, hsj = cells[j][1:3]
            if cj == h and ci in hsj:
                agreements.append((i,j))
                break
        else:
            continue
        break

output_format = '{} ({})'
for i, j in agreements:
    worksheet.update_cell(row_from + i, 4, output_format.format(*cells[j][:2]))
    worksheet.update_cell(row_from + j, 4, output_format.format(*cells[i][:2]))
