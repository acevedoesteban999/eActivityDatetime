/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { formatFloatTime } from "@web/views/fields/formatters";
import { parseFloatTime } from "@web/views/fields/parsers";
import { useInputField } from "@web/views/fields/input_field_hook";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useNumpadDecimal } from "@web/views/fields/numpad_decimal_hook";
import { user } from "@web/core/user";

import { Component } from "@odoo/owl";

export class FloatTimeTZ extends Component {
    static template = "e_activity_crm.FloatTimeTZ";
    static props = {
        ...standardFieldProps,
        inputType: { type: String, optional: true },
        displaySeconds: { type: Boolean, optional: true },
    };
    static defaultProps = {
        inputType: "text",
    };

    setup() {
        this.user_tz = user?.tz || "UTC";

        this.inputFloatTimeRef = useInputField({
            getValue: () => this.formattedValue,
            refName: "numpadDecimal",
            parse: (v) => {
                let userValue = parseFloatTime(v);
                if (userValue < 0 || userValue >= 24)
                    throw new Error(_t("Time must be between 00:00 and 23:59"));
                return this.userTZToUTC(userValue);
            },
        });

        useNumpadDecimal();
    }

    get formattedValue() {
        const utcValue = this.props.record.data[this.props.name];
        const userValue = this.utcToUserTZ(utcValue);
        return formatFloatTime(userValue, {
            displaySeconds: this.props.displaySeconds,
        });
    }

    utcToUserTZ(utcValue) {
        if (this.user_tz === "UTC" || !utcValue) return utcValue;

        const now = new Date();
        const utcDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        utcDate.setUTCHours(Math.floor(utcValue), (utcValue % 1) * 60, 0, 0);

        const userDate = new Date(utcDate.toLocaleString("en-US", { timeZone: this.user_tz }));
        const utcDateCheck = new Date(utcDate.toLocaleString("en-US", { timeZone: "UTC" }));
        const offset = (userDate - utcDateCheck) / (1000 * 60 * 60);

        return utcValue + offset;
    }

    userTZToUTC(userValue) {
        if (this.user_tz === "UTC" || !userValue) return userValue;

        const now = new Date();
        const userDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        userDate.setHours(Math.floor(userValue), (userValue % 1) * 60, 0, 0);

        const utcDate = new Date(userDate.toLocaleString("en-US", { timeZone: "UTC" }));
        const userDateCheck = new Date(userDate.toLocaleString("en-US", { timeZone: this.user_tz }));
        const offset = (userDateCheck - utcDate) / (1000 * 60 * 60);

        return userValue - offset;
    }
}

export const floatTimeTzField = {
    component: FloatTimeTZ,
    displayName: _t("Time (TZ)"),
    supportedOptions: [
        {
            label: _t("Display seconds"),
            name: "display_seconds",
            type: "boolean",
        },
        {
            label: _t("Type"),
            name: "type",
            type: "string",
            default: "text",
        },
    ],
    supportedTypes: ["float"],
    isEmpty: () => false,
    extractProps: ({ options }) => ({
        displaySeconds: options.display_seconds,
        inputType: options.type,
    }),
};

registry.category("fields").add("float_time_tz", floatTimeTzField);