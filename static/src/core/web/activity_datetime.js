import { patch } from '@web/core/utils/patch';
import { Activity } from '@mail/core/web/activity';
import { getMsToTomorrow } from "@mail/utils/common/dates";
import { browser } from "@web/core/browser/browser";
import { formatDateTime } from "@web/core/l10n/dates";
import { user } from "@web/core/user";
const { DateTime } = luxon;


patch(Activity.prototype,{
    setup() {
        super.setup(...arguments);
    },
    get datetimeDeadLine(){
        return formatDateTime(this.props.activity.datetime_deadline,{format:"HH:mm",tz:user.tz})
    },
    get delayTime(){
        return this.props.activity.datetime_deadline.diff(DateTime.now())
    },
    updateDelayAtEventOrNight(){
        browser.clearTimeout(this.updateDelayMidnightTimeout);
        
        const deadline = this.props.activity.datetime_deadline || this.props.activity.date_deadline;
        
        if (!deadline) {
            this.updateDelayMidnightTimeout = browser.setTimeout(
                () => this.render(),
                getMsToTomorrow() + 100
            );
            return;
        }
        
        const now = DateTime.now();
        const delay = this.delay;
        let msUntilUpdate;
        
        if (delay === 0) {
            const msToEvent = deadline.diff(now, "milliseconds").milliseconds;
            msUntilUpdate = msToEvent > 0 ? msToEvent : getMsToTomorrow();
            console.log(msUntilUpdate)
        } else 
            msUntilUpdate = getMsToTomorrow();
        
        this.updateDelayMidnightTimeout = browser.setTimeout(
            () => this.render(),
            msUntilUpdate + 100
        );
    },
    //Now Update At Nigth or in Event
    updateDelayAtNight() {
        this.updateDelayAtEventOrNight()
    },

    async edit(){
        super.edit();
        this.updateDelayAtEventOrNight();
    }

    
});
