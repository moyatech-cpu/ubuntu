from odoo import fields, http, tools, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager


class KnowledgeManagementController(http.Controller):

    @http.route(['/knowledge/documents', '/knowledge/documents/page/<int:page>'], type='http', auth="user", website=True)
    def portal_knowledge_documents(self, page=1, sortby=None, **kw):
        KnowledgeManagement = request.env['knowledge.management']
        KnowledgeManagementCount = KnowledgeManagement.search_count([('state', '=', 'publish'), ('group_ids', 'in', request.env.user.groups_id.ids)])
        pager = portal_pager(
            url="/knowledge/documents",
            total=KnowledgeManagementCount,
            page=page,
            step=12
        )
        knowledge_managements = KnowledgeManagement.search([('state','=','publish'),('group_ids','in',request.env.user.groups_id.ids)], limit=12, offset=pager['offset'])
        values = {
            'documents': knowledge_managements.sudo(),
            'pager': pager,
            'default_url': '/knowledge/documents',
            'page_name': 'document',
        }
        return request.render("nyda_knowledge_management.portal_documents", values)

    @http.route(['/knowledge/documents/<int:order>'], type='http', auth="public", website=True)
    def portal_knowledge_page(self, order=None, access_token=None, **kw):
        document = request.env['knowledge.management'].browse([order])
        values = {'document':document,
                  'page_name': 'document'}
        return request.render("nyda_knowledge_management.portal_document_page", values)






