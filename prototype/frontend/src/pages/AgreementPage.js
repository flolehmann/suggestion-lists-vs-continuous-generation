import { useState } from "react";
import { DataPolicy } from "../js_components/Agreement";
import { Link } from "react-router-dom";

export function AgreementPage() {
    const [checked, setChecked] = useState(false)

    const handleChange = () => {
        setChecked(!checked)
    }

    let li
    if (checked) { 
        li = <Link to='/task0'> Start </Link>
    }
    else {
        li = <label> Start </label>
    }

    return(
        <>
        <h1> Agreement </h1>
        <label> Before starting the tasks you have to agree to the "Statutory Disclosure Duty for the Collection of Data Act 13 GDPR". </label>
        <div className='smallSpace'/>
        <div className='scrollBox'>
            <DataPolicy />
        </div>
        <div className='smallSpace'/>
        <div>
            <input 
                type='checkbox' 
                checked={checked}
                onChange={handleChange}
            />
            <label>I have read the "Statutory Disclosure Duty for the Collection of Data Act 13 GDPR" above and agree to it</label>
        </div>
        <div className='smallSpace'/>
        {li}
        </>
    )
}
