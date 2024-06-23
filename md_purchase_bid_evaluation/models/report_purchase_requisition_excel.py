# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date, timedelta, datetime
import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import tempfile
from odoo.tools.misc import xlwt
import io
import base64
import time
from dateutil.relativedelta import relativedelta
from pytz import timezone
import re
from PIL import Image

class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    def print_purchase_requisition_excel_report_abtis(self):
        filename = 'Purchase Requisition Report of ' + str(self.name) + '.xls'
        workbook = xlwt.Workbook()

        worksheet = workbook.add_sheet('Tender')
        font = xlwt.Font()
        font.bold = True
        for_left = xlwt.easyxf("font: bold 1, color black; borders: top double, bottom double, left double, right double; align: horiz left")
        for_right = xlwt.easyxf("font: bold 1, color black; borders: top double, bottom double, left double, right double; align: horiz right")
        for_left_center = xlwt.easyxf("font: bold 1, color black; borders: top double, bottom double, left double, right double; align: horiz center")
        for_left_not_bold = xlwt.easyxf("font: color black; align: horiz left")
        for_right_not_bold = xlwt.easyxf("font: color black; align: horiz right")
        for_center_bold = xlwt.easyxf("font: bold 1, color black; align: horiz center")
        for_left_bold = xlwt.easyxf("font: bold 1, color black; align: horiz left")
        for_center = xlwt.easyxf("font: bold 1, color black; borders: top double, bottom double, left double, right double; align: horiz center")
        GREEN_TABLE_HEADER = xlwt.easyxf(
                 'font: bold 1, name Tahoma, height 250;'
                 'align: vertical center, horizontal center, wrap on;'
                 'borders: top double, bottom double, left double, right double;'
                 )
        style = xlwt.easyxf('font:height 400, bold True, name Arial; align: horiz center, vert center;borders: top medium,right medium,bottom medium,left medium')
        
        alignment = xlwt.Alignment()  # Create Alignment
        alignment.horz = xlwt.Alignment.HORZ_RIGHT
        style = xlwt.easyxf('align: wrap yes')
        style.num_format_str = '0.00'

        worksheet.row(0).height = 320
        worksheet.col(0).width = 2000
        worksheet.col(1).width = 10000
        worksheet.col(2).width = 3000
        worksheet.col(3).width = 3000
        worksheet.col(4).width = 3000
        worksheet.col(5).width = 3000
        worksheet.col(6).width = 3000
        worksheet.col(7).width = 4000
        worksheet.col(8).width = 3000
        worksheet.col(9).width = 4000
        worksheet.col(10).width = 3000
        worksheet.col(11).width = 4000
        worksheet.col(12).width = 3000
        worksheet.col(13).width = 4000
        worksheet.col(14).width = 3000
        worksheet.col(15).width = 4000
        borders = xlwt.Borders()
        borders.bottom = xlwt.Borders.MEDIUM
        border_style = xlwt.XFStyle()  # Create Style
        border_style.borders = borders

        row = 1
        tendor_name = 'TENDER NO' + ' - ' + str(self.name)
        worksheet.write_merge(row, row+1, 0, 5+(self.order_count * 2), tendor_name or '', GREEN_TABLE_HEADER)

        row = row + 3
        worksheet.write_merge(row, row+1, 0, 0, 'Item No' or '', for_center)
        worksheet.write_merge(row, row+1, 1, 1, 'Description' or '', for_center)
        worksheet.write_merge(row, row+1, 2, 2, 'Item Code' or '', for_center)
        worksheet.write_merge(row, row+1, 3, 3, 'Last PO\nUnit Price' or '', for_center)
        worksheet.write_merge(row, row+1, 4, 4, 'Qty' or '', for_center)
        worksheet.write_merge(row, row+1, 5, 5, 'Unit' or '', for_center)
        col = 6
        purchase_order_ids = self.env['purchase.order'].search([('requisition_id', '=', self.id)])
        for purchase_order_supplier in purchase_order_ids:
            worksheet.write_merge(row, row, col, col+1, purchase_order_supplier.partner_id.name or '', for_center)
            col += 2
        row = row + 1
        col = 6
        for purchase_order_unit_price_total_amt in purchase_order_ids:
            worksheet.write(row, col, 'Unit Price' or '', for_center)
            worksheet.write(row, col+1, 'Total Amount' or '', for_center)
            col += 2

        seq = 1
        for line in self.line_ids:
            row = row + 1
            worksheet.write(row, 0, seq or '', for_right_not_bold)
            seq += 1
            worksheet.write(row, 1, line.product_id.name or '', for_left_not_bold)
            worksheet.write(row, 2, line.product_id.default_code or '', for_left_not_bold)
            worksheet.write(row, 3, '', for_right_not_bold)
            worksheet.write(row, 4, line.product_qty or '', for_right_not_bold)
            worksheet.write(row, 5, line.product_uom_id.name or '', for_left_not_bold)
            col = 6
            for purchase_order_unit_price_total_amt_display in purchase_order_ids:
                for purchase_line in purchase_order_unit_price_total_amt_display.order_line:
                    if purchase_line.product_id.id == line.product_id.id:
                        price_unit_currency = ''
                        total_price_currency = ''
                        if purchase_order_unit_price_total_amt_display.currency_id.position == 'before':
                            price_unit_currency = str(purchase_order_unit_price_total_amt_display.currency_id.symbol) + ' ' + str(purchase_line.price_unit)
                            total_price_currency = str(purchase_order_unit_price_total_amt_display.currency_id.symbol) + ' ' + str(purchase_line.price_subtotal)
                        else:
                            price_unit_currency = str(purchase_line.price_unit) + ' ' + str(purchase_order_unit_price_total_amt_display.currency_id.symbol)
                            total_price_currency = str(purchase_line.price_subtotal) + ' ' + str(purchase_order_unit_price_total_amt_display.currency_id.symbol)
                        worksheet.write(row, col, price_unit_currency or '', for_right_not_bold)
                        worksheet.write(row, col+1, total_price_currency or '', for_right_not_bold)
                        col += 2

        row = row + 2
        worksheet.write_merge(row, row, 0, 5, 'Total Amount:' or '', for_left)
        col = 6
        for purchase_order_total_amount in purchase_order_ids:
            if purchase_order_total_amount.currency_id.position == 'before':
                amount_untaxed_currency = str(purchase_order_total_amount.currency_id.symbol) + ' ' + str(purchase_order_total_amount.amount_untaxed)
            else:
                amount_untaxed_currency = str(purchase_order_total_amount.amount_untaxed) + ' ' + str(purchase_order_total_amount.currency_id.symbol)
            worksheet.write_merge(row, row, col, col+1, amount_untaxed_currency or '', for_center)
            col += 2

        row = row + 1
        worksheet.write_merge(row, row, 0, 5, 'VAT:' or '', for_left)
        col = 6
        for purchase_order_vat in purchase_order_ids:
            if purchase_order_vat.currency_id.position == 'before':
                amount_tax_currency = str(purchase_order_vat.currency_id.symbol) + ' ' + str(purchase_order_vat.amount_tax)
            else:
                amount_tax_currency = str(purchase_order_vat.amount_tax) + ' ' + str(purchase_order_vat.currency_id.symbol)
            worksheet.write_merge(row, row, col, col+1, amount_tax_currency or '', for_center)
            col += 2

        row = row + 1
        worksheet.write_merge(row, row, 0, 5, 'Grand Total:' or '', for_left)
        col = 6
        for purchase_order_grand_total in purchase_order_ids:
            if purchase_order_grand_total.currency_id.position == 'before':
                amount_total_currency = str(purchase_order_grand_total.currency_id.symbol) + ' ' + str(purchase_order_grand_total.amount_total)
            else:
                amount_total_currency = str(purchase_order_grand_total.amount_total) + ' ' + str(purchase_order_grand_total.currency_id.symbol)
            worksheet.write_merge(row, row, col, col+1, amount_total_currency or '', for_center)
            col += 2

        row = row + 1
        worksheet.write_merge(row, row, 0, 5, 'Remarks:' or '', for_left)
        col = 6
        for purchase_order_remarks in purchase_order_ids:
            worksheet.write_merge(row, row, col, col+1, purchase_order_remarks.notes or '', for_center)
            col += 2

        row = row + 1
        worksheet.write_merge(row, row, 0, 5, 'Delivery Terms:' or '', for_left)
        col = 6
        for purchase_order_delivery_terms in purchase_order_ids:
            worksheet.write_merge(row, row, col, col+1, '', for_center)
            col += 2

        row = row + 1
        worksheet.write_merge(row, row, 0, 5, 'Payment Terms:' or '', for_left)
        col = 6
        for purchase_order_payment_terms in purchase_order_ids:
            worksheet.write_merge(row, row, col, col+1, purchase_order_payment_terms.payment_term_id.name or '', for_center)
            col += 2

        row = row + 1
        worksheet.write_merge(row, row, 0, 5, 'Delivery Period/Time:' or '', for_left)
        col = 6
        for purchase_order_delivery_period_time in purchase_order_ids:
            worksheet.write_merge(row, row, col, col+1, '', for_center)
            col += 2

        row = row + 3
        lowest_price_supplier = ''
        lowest_price_check = purchase_order_ids[0].amount_total
        for purchase_order_check_lowest_amount_supplier in purchase_order_ids:
            if purchase_order_check_lowest_amount_supplier.amount_total <= lowest_price_check:
                lowest_price_supplier = 'Recommended Supplier:  ' + str(purchase_order_check_lowest_amount_supplier.partner_id.name)
        worksheet.write_merge(row, row, 0, 5+(self.order_count * 2), lowest_price_supplier or '', for_left)

        row = row + 1
        worksheet.write_merge(row, row, 0, 5+(self.order_count * 2), 'Reasons for recommendation: Lowest price' or '', for_left)

        row = row + 1
        tender_remarks = 'Remarks: ' + str(self.description) 
        worksheet.write_merge(row, row, 0, 5+(self.order_count * 2), tender_remarks or '', for_left)

        row = row + 2
        worksheet.write_merge(row, row, 0, 2, 'Prepared By:' or '', for_left)
        worksheet.write_merge(row, row, 4, 6, 'Noted By:' or '', for_left)
        worksheet.write_merge(row, row, 8, 10, 'Approved By:' or '', for_left)
        row = row + 1
        worksheet.write_merge(row, row, 0, 1, '', for_left)
        worksheet.write(row, 2, '', for_left)
        worksheet.write_merge(row, row, 4, 5, '', for_left)
        worksheet.write(row, 6, '', for_left)
        worksheet.write_merge(row, row, 8, 9, '', for_left)
        worksheet.write(row, 10, '', for_left)
        row = row + 1
        worksheet.write_merge(row, row, 0, 1, 'Purchase Officer' or '', for_left)
        worksheet.write(row, 2, 'Date' or '', for_left)
        worksheet.write_merge(row, row, 4, 5, 'Finance Manager' or '', for_left)
        worksheet.write(row, 6, 'Date' or '', for_left)
        worksheet.write_merge(row, row, 8, 9, 'General Manager' or '', for_left)
        worksheet.write(row, 10, 'Date' or '', for_left)


        fp = io.BytesIO()
        workbook.save(fp)
        purchase_requisition_excel_id = self.env['abtis.purchase.requisition.report.excel.extended'].create({'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename})
        fp.close()

        return{
            'view_mode': 'form',
            'res_id': purchase_requisition_excel_id.id,
            'res_model': 'abtis.purchase.requisition.report.excel.extended',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'context': self._context,
            'target': 'new',
        }


class AbtisPurchaseRequisitionReportExcelExtended(models.Model):
    _name = 'abtis.purchase.requisition.report.excel.extended'
    _description = "Purchase Requisition Report Excel Extended"

    excel_file = fields.Binary('Download Report :- ')
    file_name = fields.Char('Excel File', size=64)
