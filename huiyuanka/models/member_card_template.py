# -*- coding: utf-8 -*-

from odoo import models, fields, api


# 会员卡 实体
# 会员卡 类别 类别1 类别2 类别3 类别4 类别5
# 会员卡
class memberCardTemplate(models.Model):

    _name = 'member.card.template'
    # 折扣 办卡描述 使用描述 类别
    def _get_default_category_id(self):
        if self._context.get('categ_id') or self._context.get('default_categ_id'):
            return self._context.get('categ_id') or self._context.get('default_categ_id')
        category = self.env.ref('member.card.member_card_category_all', raise_if_not_found=False)
        if not category:
            category = self.env['member.card.category'].search([], limit=1)
        if category:
            return category.id
        else:
            err_msg = _('You must define at least one product category in order to be able to create products.')
            redir_msg = _('Go to Internal Categories')
            # raise RedirectWarning(err_msg, self.env.ref('product.product_category_action_form').id, redir_msg)

    name = fields.Char('Name', index=True, required=True, translate=True)

    sequence = fields.Integer('Sequence', default=1, help='Gives the sequence order when displaying a product list')

    description = fields.Text(
        'Description', translate=True)

    description_purchase = fields.Text(
        'Purchase Description', translate=True)

    description_sale = fields.Text(
        'Sale Description', translate=True,
        help="A description of the Product that you want to communicate to your customers. "
             "This description will be copied to every Sales Order, Delivery Order and Customer Invoice/Credit Note")

    type = fields.Selection([
        ('打折会员卡','返现会员卡'),
        ('预付费会员卡','积分会员卡')], string='Card Type', default='打折会员卡', required=True,
        help='')

    categ_id = fields.Many2one(
        'member.card.category', 'Member Card Category',
        change_default=True, default=_get_default_category_id,
        required=True, help="Select category for the current product")

    currency_id = fields.Many2one(
        'res.currency', 'Currency', compute='_compute_currency_id')

    cost_currency_id = fields.Many2one(
        'res.currency', 'Cost Currency', compute='_compute_cost_currency_id')

    discount = fields.Integer(string="折扣", required=False)
    discount_product_category  = fields.Many2one(comodel_name="product.category", string="折扣产品类目", required=False)
    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary(
        "Image", attachment=True,
        help="This field holds the image used as image for the product, limited to 1024x1024px.")
    image_medium = fields.Binary(
        "Medium-sized image", attachment=True,
        help="Medium-sized image of the product. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved, "
             "only when the image exceeds one of those sizes. Use this field in form views or some kanban views.")
    image_small = fields.Binary(
        "Small-sized image", attachment=True,
        help="Small-sized image of the product. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")

    @api.multi
    def _compute_currency_id(self):
        main_company = self.env['res.company']._get_main_company()
        for template in self:
            template.currency_id = template.company_id.sudo().currency_id.id or main_company.currency_id.id

    def _compute_cost_currency_id(self):
        for template in self:
            template.cost_currency_id = self.env.user.company_id.currency_id.id