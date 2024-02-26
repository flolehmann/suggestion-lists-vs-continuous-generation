import { TaskDisplay } from "../js_components/TaskDisplay";
import React, {useState, useEffect} from "react";
import { useParams } from "react-router";
import { Link } from "react-router-dom";
import { BACKEND_URL } from "../App";

export function TaskPage(props) {
    const { tid } = useParams()
    const [task, setTask] = useState([])

    useEffect(() => {
        fetch(`${BACKEND_URL}/api/task/${tid}`)
        .then(response => response.json())
        .then(data => setTask(data))
    }, [tid])

    return(
        <>
        <TaskDisplay task={task.desc}/>
        <div>
            <h3> Method: </h3>
            {task.method_name}
        </div>
        <div>
            <div className='divider'/>
            <Link to={'/task'+tid+'/writing'} className='link'> Start </Link>
        </div>
        </>
    )
}