import TextField from '../js_components/TextField'
import { ControllButtons } from '../js_components/ControllButtons'
import Baseline from './Baseline'

class Version1 extends Baseline {

    render() {
        this.props.set_length(this.state.sentence.length)
        return(
            <>
            <div>
                <TextField 
                    start={this.startClock} 
                    stop={this.stopClock}
                    on_submit={()=>{}} 
                    sentence={this.state.sentence} 
                    handle_typing={this.handle_typing}
                    set_len={()=>{}}
                    disabled={this.state.isGenerating}
                />
            </div>
            <div>
                <ControllButtons 
                    startClock={this.triggerStart} 
                    stopClock={this.stopClock}
                    redoGeneration={this.redoGeneration}
                    slowerGeneration={this.slowerGeneration}
                    fasterGeneration={this.fasterGeneration}
                    disabled={this.state.isGenerating}
                    running={this.state.running}
                />
            </div>
            </>
        );
    }
}

export default Version1;