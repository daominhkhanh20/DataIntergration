import constain from '../../constrain/index'

var initState = {
    brandFilters: [],
    selectedBrandFilter: [],
    fromPrice: "",
    toPrice: "",
    RAMFilters: [],
    selectedRAMFilter: [],
    storageFilters: [],
    selectedStorageFilter: [],
    totalPage: 1,
    currentPage: 1,
    searchString: "",
    items: []
}

var homeReducer = (state = initState, action) => {
    switch (action.type) {
        case constain.SET_STATES:
            return {
                ...state,
                ...action
            }
        default:
            return state
    }
}

export default homeReducer