from odoo import api, models

ACCOUNTING_MENU_ICON = 'om_account_accountant,static/description/acc-icon.png'
ACCOUNTING_NAME = {'en': 'Accounting', 'ar': 'المحاسبة'}


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def _om_accountant_apply_branding(self):
        """Always show the accounting app as «المحاسبة» / "Accounting" with the
        module icon. Runs on every install/upgrade (data/branding.xml) because
        translations already stored in the database (e.g. «الفوترة» from the
        account module) are not overwritten by .po files."""
        menu = self.env.ref('account.menu_finance', raise_if_not_found=False)
        if not menu:
            return
        if menu.web_icon != ACCOUNTING_MENU_ICON:
            menu.web_icon = ACCOUNTING_MENU_ICON
        installed = [code for code, _name in self.env['res.lang'].get_installed()]
        arabic = [code for code in installed if code.split('_')[0] == 'ar']
        names = {'en_US': ACCOUNTING_NAME['en']}
        names.update({code: ACCOUNTING_NAME['ar'] for code in arabic})
        menu.update_field_translations('name', names)
        view = self.env.ref('om_account_accountant.res_config_settings_view_form', raise_if_not_found=False)
        if view and arabic:
            view.update_field_translations(
                'arch_db', {code: {ACCOUNTING_NAME['en']: ACCOUNTING_NAME['ar']} for code in arabic})
