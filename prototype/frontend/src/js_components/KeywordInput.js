import '../App.css';

export function KeywordInput(props) {

    const handleSubmit = (event) => {
        event.preventDefault();
        let keyword = document.getElementById('input').value
        props.generate(keyword)
    }

    var lbl
    if(props.disabled) {
        lbl = 'Generating...'
    }
    else {
        lbl = '. . .'
    }

    return (
        <>
            <form onSubmit={handleSubmit}>
                <input type='text' id='input' className='KeywordInput' disabled={props.disabled} required></input>
                <input type='submit' value='Generate' disabled={props.disabled} style={{ margin: 3 }}></input>
            </form>
            <label id='status_lbl'> {lbl} </label>
        </>
    )
}