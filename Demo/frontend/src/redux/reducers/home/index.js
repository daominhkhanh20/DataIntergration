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
    totalPage: 9,
    currentPage: 1,
    searchString: "",
    items: [],
    onlyGetMatchingData: true,
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