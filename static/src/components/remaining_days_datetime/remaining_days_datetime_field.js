/** @odoo-module **/

import { registry } from "@web/core/registry";
import { RemainingDaysField , remainingDaysField } from "@web/views/fields/remaining_days/remaining_days_field";

export class ERemainingDaysDatetime extends RemainingDaysField {
    setup() {
    }
    
    get dateTimeValue(){
      if(!this.props.record.data.all_day && Math.abs(this.diffDays) <= 2)
        return " (" + this.props.record.data.datetime_deadline.toFormat('HH:mm') + ")";
      return ""
    }

    get diffString() {
        return super.diffString + this.dateTimeValue;  
    }

    get numericValue() {
      return super.numericValue + this.dateTimeValue
    }
}

const eremainingDaysDatetime = {
  ...remainingDaysField,
  component: ERemainingDaysDatetime,
};

registry.category("fields").add("eremaining_days_datetime", eremainingDaysDatetime);
