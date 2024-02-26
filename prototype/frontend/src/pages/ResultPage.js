import React, {useState, useEffect} from "react";
import { Link } from "react-router-dom";
import { useParams } from "react-router";
import './ResultPage.css'
import { BACKEND_URL } from "../App";

import { TaskDisplay } from "../js_components/TaskDisplay";

export function ResultPage() {

    const { tid } = useParams()
    const [task, setTask] = useState([])
    const [quests, setQuests] = useState([])

    useEffect(() => {
        fetch(`${BACKEND_URL}/api/task/${tid}`)
        .then(response => response.json())
        .then(data => setTask(data))

        fetch(`${BACKEND_URL}/api/questions`)
        .then(response => response.json())
        .then(data => setQuests(data.questions))

        return () => {
            fetch(`${BACKEND_URL}/api/task/${tid}/store`)
        }
    }, [tid])

    const handle_change = (i) => {
        const rbs = document.getElementsByName('rating'+i);
        let selectedValue = 0;
        for (const rb of rbs) {
            
            if (rb.checked) {
                selectedValue = rb.value;
                break;
            }
        }

        fetch(`${BACKEND_URL}/api/task/${tid}/rating`, {
            method: 'POST',
            body: JSON.stringify({
                'index' : i,
                'rating': parseInt(selectedValue)
            }),
            headers: {
                "Content-type": "aplication/json; charset=UTF-8"
              }
          })
    }

    let questions = []
    for(let i=0; i<quests.length; i++) {
        questions.push(
            <form onChange={() => handle_change(i)} key={i}>
                <label className='questionlabel'> {quests[i]} </label> <br/>
                <label className='radiolabel'><input type="radio" name={'rating'+i} value={1} /> Strongly disagree </label>
                <label className='radiolabel'><input type="radio" name={'rating'+i} value={2} /> Disagree </label>
                <label className='radiolabel'><input type="radio" name={'rating'+i} value={3} /> Neither agr. nor disagr. </label>
                <label className='radiolabel'><input type="radio" name={'rating'+i} value={4} /> Agree </label>
                <label className='radiolabel'><input type="radio" name={'rating'+i} value={5} /> Strongly agree </label>
            </form>)
    }


    let link
    if (!task.last) {
        link = <Link to={'/task'+(parseInt(tid)+1)} className='link'> Next </Link>
    }
    else {
        link = <Link to='/finished' className='link'> Finish </Link>
    }

    return(
        <>
        <TaskDisplay task={task.desc}/>
        <div>
            <h3> Your Result: </h3>
            {task.result}
            <div className='divider'/>     
        </div>   
        <div>
            <h3> Questions </h3>
            {questions}
        </div>
        
        {link}
        <div className='divider'/>
        </>
    )
}