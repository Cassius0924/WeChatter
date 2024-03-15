import React from 'react';
import { Form, FormCell, CellHeader, Label, CellBody, Input, CellFooter, Icon } from 'react-weui';

export function isValueExist(value) {
    if (typeof value === 'string') {
        return value !== '';
    } else if (Array.isArray(value)) {
        return value.length > 0 && value.every(v => v !== '');
    } else {
        return false;
    }
}

function CustomFormCell({ label, value, onChange, placeholder = null, iconValues = { success: "success", cancel: "cancel" } }) {
    const headerStyle = {
        width: '20%',
        paddingRight: '10px',
        whiteSpace: 'nowrap'
    };

    const bodyStyle = {
        width: '80%'
    };

    return (
        <Form>
            <FormCell>
                <CellHeader style={headerStyle}>
                    <Label>{label}</Label>
                </CellHeader>
                <CellBody style={bodyStyle}>
                    <Input
                        type="text"
                        placeholder={placeholder}
                        value={value || ''}
                        onChange={onChange}
                    />
                </CellBody>
                {/*TODO: 查看有多少个空value，在收集，并在app.js里加入<Badge preset="body">8</Badge>*/}
                <CellFooter>
                    {isValueExist(value) ? <Icon value={iconValues.success}/> : <Icon value={iconValues.cancel}/>}
                </CellFooter>
            </FormCell>
        </Form>
    );
}

export default CustomFormCell;
