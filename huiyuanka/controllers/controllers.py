# -*- coding: utf-8 -*-
from odoo import http

# class Huiyuanka(http.Controller):
#     @http.route('/huiyuanka/huiyuanka/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/huiyuanka/huiyuanka/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('huiyuanka.listing', {
#             'root': '/huiyuanka/huiyuanka',
#             'objects': http.request.env['huiyuanka.huiyuanka'].search([]),
#         })

#     @http.route('/huiyuanka/huiyuanka/objects/<model("huiyuanka.huiyuanka"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('huiyuanka.object', {
#             'object': obj
#         })