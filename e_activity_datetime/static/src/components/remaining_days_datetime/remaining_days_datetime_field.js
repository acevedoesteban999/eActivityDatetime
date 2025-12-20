/** @odoo-module **/

import { registry } from "@web/core/registry";
import { evaluateExpr } from "@web/core/py_js/py";
import { getClassNameFromDecoration } from "@web/views/utils";
import { RemainingDaysField , remainingDaysField } from "@web/views/fields/remaining_days/remaining_days_field";
import { formatDate } from "@web/views/fields/formatters";
import { capitalize } from "@web/core/utils/strings";
import { _t } from "@web/core/l10n/translation";
const { DateTime } = luxon;

export class ERemainingDaysDatetime extends RemainingDaysField {
    setup() {
      this.props.classesTimeDate = {
        ...this.props.classes,
        danger:"days < 0 or (days == 0 and passEventTime)",
        warning:"days == 0 and not passEventTime",
      }
    }
    
    get diffDays() {
      if(!this.props.record.data.all_day){
        const today = DateTime.local().startOf("day");
        const diff = this.props.record.data.datetime_deadline.startOf("day").diff(today, "days");
        return Math.floor(diff.days);
      }
      return super.diffDays   
    }

    get classNames() {
      if(!this.props.record.data.all_day){
        if (this.diffDays === null) {
          return null;
        }
        if (!this.props.record.isActive) {
            return null;
        }
        const classNames = {};
        const evalContext = { days: this.diffDays, record: this.props.record.evalContext,passEventTime: this.props.record.data.datetime_deadline < DateTime.now() };
        for (const decoration in this.props.classesTimeDate) {
            const value = evaluateExpr(this.props.classesTimeDate[decoration], evalContext);
            classNames[getClassNameFromDecoration(decoration)] = value;
        }
        return classNames;
      }
      return super.classNames
      
    }
    get showDatetimeStart(){
        return this.props.record.data.datetime_start && this.props.record.data.datetime_start.day == this.props.record.data.datetime_deadline.day
    }
    get dateTimeValue(){
      if(!this.props.record.data.all_day && Math.abs(this.diffDays) <= 2){
        if(this.showDatetimeStart)
          return " (" + this.props.record.data.datetime_start.toFormat('HH:mm ') + _t('to') + this.props.record.data.datetime_deadline.toFormat(' HH:mm') + ")";
        return " (" + this.props.record.data.datetime_deadline.toFormat('HH:mm') + ")";
      }
      return ""
    }

    get formattedValue() {
      if(!this.props.record.data.all_day){
          return formatDate(this.props.record.data.datetime_deadline, { numeric: true });
      }
      return super.formattedValue
    }

    get diffString() {
      if(!this.props.record.data.all_day){
        if (this.diffDays === null) {
            return "";
        }
        if (Math.abs(this.diffDays) > 99) {
            return this.formattedValue;
        }
        return capitalize(this.props.record.data.datetime_deadline.toRelativeCalendar()) + this.dateTimeValue;
      }
      return super.diffString + this.dateTimeValue;  
    }

    get numericValue() {
      if(!this.props.record.data.all_day){
        return formatDate(this.props.record.data.datetime_deadline, { numeric: true }) + this.dateTimeValue;
      }
      return super.numericValue + this.dateTimeValue
    }
}

const eremainingDaysDatetime = {
  ...remainingDaysField,
  component: ERemainingDaysDatetime,
};

registry.category("fields").add("eremaining_days_datetime", eremainingDaysDatetime);
