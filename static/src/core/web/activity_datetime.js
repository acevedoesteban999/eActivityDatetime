import { patch } from '@web/core/utils/patch';
import { Activity } from '@mail/core/web/activity';
import { computeDelay } from "@mail/utils/common/dates";
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
    get millisecondToFullMinit(){
        return 1000*(60 - this.props.activity.datetime_deadline.second)
    },
    get delay() {
        if(!this.props.activity.all_day)
            return Math.floor(computeDelay(this.props.activity.datetime_deadline));
        return super.delay;
    },
    get delayTime(){
        return this.props.activity.datetime_deadline.diff(DateTime.now()) + this.millisecondToFullMinit
    },
    updateDelayAtEventOrNight(){
        browser.clearTimeout(this.updateDelayMidnightTimeout);
        if (this.props.activity.datetime_deadline && this.delay === 0) {
            let msUntilUpdate = this.delayTime
            if( msUntilUpdate > 0){
                this.updateDelayMidnightTimeout = browser.setTimeout(
                    () => {
                        this.render();
                        super.updateDelayAtNight();
                    },
                    msUntilUpdate + 100
                );
                return
            }
        } 
        super.updateDelayAtNight();
    },
    //Now Update At Nigth or in Event
    updateDelayAtNight() {
        if(!this.props.activity.all_day)
            this.updateDelayAtEventOrNight()
        else
            super.updateDelayAtNight()
    },

        async edit(){
            await super.edit();
            let datetime_deadline = await this.orm.read("mail.activity", [this.props.activity.id], ["datetime_deadline"]);
            this.props.activity.datetime_deadline = datetime_deadline[0].datetime_deadline;
            this.updateDelayAtNight();
        }

    
});
