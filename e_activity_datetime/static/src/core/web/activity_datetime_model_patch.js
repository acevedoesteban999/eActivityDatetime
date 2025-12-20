import { patch } from '@web/core/utils/patch';
import { Activity } from "@mail/core/common/activity_model";
import { fields } from "@mail/core/common/record";
import { formatDate, formatDateTime } from "@web/core/l10n/dates";


patch(Activity.prototype,{
    setup() {
        super.setup(...arguments);
        this.datetime_deadline = fields.Datetime();
        this.datetime_start = fields.Datetime();
    },
    
    get dateDeadlineFormatted() {
        if(!this.all_day)
            return formatDateTime(this.datetime_deadline);
        return formatDate(this.date_deadline);
    },
});
