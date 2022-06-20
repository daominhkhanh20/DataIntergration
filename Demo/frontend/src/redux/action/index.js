import constain from '../constrain/index'

export const setStates = (data) => {
    return {
        type: constain.SET_STATES,
        ...data
    }
}