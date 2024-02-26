export function TaskDisplay(props) {

    return(
        <>
            <h3> Your Task: </h3>
            {props.task}
            <div className='divider'/> 
        </>
    )
} 