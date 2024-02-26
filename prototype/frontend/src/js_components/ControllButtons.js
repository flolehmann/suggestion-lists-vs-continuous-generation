import '../App.css';

export function ControllButtons(props) {

    return(
        <>
          <button onClick={props.startClock}  disabled={props.disabled || props.running}  className='cButton'> Continue </button>
          <button onClick={props.stopClock}   disabled={props.disabled || !props.running} className='cButton'> Stop </button>
        </>
    )
    /*
      <button onClick={props.redoGeneration}    disabled={props.disabled}> Redo </button>
      <button onClick={props.slowerGeneration}  disabled={props.disabled}> {'<<'} </button>
      <button onClick={props.fasterGeneration}  disabled={props.disabled}> {'>>'} </button>
    */
}