import React, { useState } from "react";
import { Link } from "react-router-dom";
import { BACKEND_URL } from "../App";

export function StartingPage(props) {

    const [disabled, setDisabled] = useState(true)

    const handleSubmit = (event) => {
        event.preventDefault()
        let uid = document.getElementById('uid_input').value
        fetch(`${BACKEND_URL}/api/user/${uid}`)
        .then( setDisabled(false) )
    }

    let li
    if (disabled) {
        li = <label> Tasks </label>
    }
    else {
        li = <Link to='/task0'> Tasks </Link>
    }

    return(
        <>
        <div>
            <h2> Enter your UserId </h2>
            <form onSubmit={handleSubmit}>
                <label>UserId</label> <br/>
                <input type="text" id="uid_input"/> <br/>
                <input type="submit" value="Submit"></input>
            </form>
        </div>

        <h2> Choose your version </h2>
        <li> <Link to='/version0'> Standard input </Link> </li>
        <li> <Link to='/version1'> Version1 </Link> </li>
        <li> <Link to='/version2'> Version2 </Link> </li>

        <h2> Start with tasks </h2>
        {li}
        </>
    )
}
