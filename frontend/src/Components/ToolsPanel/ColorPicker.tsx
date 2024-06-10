import React, {useState} from "react";
import './tools.css';

type Props = {
    value: string;
    onChange: (value: string) => void;
}

function hexToRgb(hex: string): { r: number, g: number, b: number } | null {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

const suggestedColors: string[] = [
    '#990000',
    '#997700',
    '#006600',
    '#000099',
    '#000000',
    '#ff2222',
    '#ff9922',
    '#22c555',
    '#2255ff',
    '#cccccc',
]

export function ColorPicker({value, onChange}: Props): React.JSX.Element {
    const [hexValue, setHexValue] = useState<string>(value);
    const [showMenu, setShowMenu] = useState(false);


    function handleHexValueChange(hex: string) {
        setHexValue(hex);
        if (!hexToRgb(hex)) {
            return;
        }
        onChange(hex);
    }

    function handleValueChange(evt: React.ChangeEvent<HTMLInputElement>) {
        handleHexValueChange(evt.target.value);
    }

    function handleBlur(evt: React.FocusEvent) {
        if (!evt.currentTarget.contains(evt.relatedTarget)) {
            setShowMenu(false)
        }
    }

    return (
        <div
            className="color-picker-icon"
            style={{backgroundColor: hexValue}}
            onClick={() => setShowMenu(true)}
            contentEditable
            onBlur={handleBlur}>
            {showMenu && (
                <div className="color-picker-menu">
                    <div className='color-options-container'>
                        {suggestedColors.map(c => (
                        <div
                            key={c}
                            className={'color-option'}
                            style={{backgroundColor: c}}
                            onClick={() => handleHexValueChange(c)}
                        />))}
                    </div>
                    <input max={7} className={'color-picker-hex'} value={hexValue} onChange={handleValueChange}/>
                </div>
            )}
        </div>);
}