import { patch } from '@web/core/utils/patch';
import { Activity } from "@mail/core/common/activity_model";
import { _t } from "@web/core/l10n/translation";


patch(Activity.prototype,{
    setup() {
        super.setup(...arguments);
    },
    async edit() {
        if(this.repeated){
            await new Promise((resolve) =>
                this.store.env.services.action.doAction(
                    {
                        type: "ir.actions.act_window",
                        name: _t("Schedule Activity"),
                        res_model: "mail.activity",
                        view_mode: "form",
                        views: [[false, "form"]],
                        target: "new",
                        res_id: this.id,
                        context: {
                            default_res_model: this.res_model,
                            default_res_id: this.res_id,
                            dialog_size: "large",
                            edit:false,
                        },
                    },
                    {
                        onClose: resolve,
                    }
                )
            );
        }
        else
            await super.edit()
    },
});
