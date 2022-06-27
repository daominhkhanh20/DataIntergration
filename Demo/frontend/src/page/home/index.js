import React, { Component } from 'react'
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
import TextField from '@mui/material/TextField';
import Card from '../../component/card';
import CircleCheckedFilled from '@material-ui/icons/CheckCircle';
import CircleUnchecked from '@material-ui/icons/RadioButtonUnchecked';
import Pagination from '@mui/material/Pagination';
import Button from '@mui/material/Button';
import './index.scss';
import { withRouter } from '../../util/withRouter';
import Header from '../../component/header';
import SearchIcon from '@mui/icons-material/Search';
import { connect } from 'react-redux';
import * as action from '../../redux/action/index';
import Api from '../../api/api';

class Home extends Component {
    constructor(props) {
        super(props);
        this.state = {}
    }
    componentDidUpdate = (preProps) => {
        if (preProps.home.currentPage !== this.props.home.currentPage) {
            //call API de lay item moi
            if(this.props.home.searchString) {
                //call APi khi co string
            }
            if (
                this.props.home.selectedBrandFilter.findIndex(() => true) !== -1 ||
                this.props.home.selectedRAMFilter.findIndex(() => true) !== -1 ||
                this.props.home.selectedStorageFilter.findIndex(() => true) !== -1
            ) {
                //call API khi co filter
            }
        }
    }

    componentDidMount = async () => {
        //call api de lay filter
        const filters = await Api.getFilter()

        //call api de lay item
        const currentPage = 1
        const pageSize = 10
        const items = await Api.getItems(currentPage, this.props.home.searchString, pageSize)

        //set state redux
        const selectedFilter = {
            selectedBrandFilter: filters.brandFilters.map(() => false),
            selectedRAMFilter: filters.RAMFilters.map(() => false),
            selectedStorageFilter: filters.storageFilters.map(() => false),
        }

        const data = { ...filters, ...items, ...selectedFilter }
        this.props.setStates(data)
    }

    checkBrandIsChecked(brand) {
        return this.state.selectedBrandFilter.find((item) => item === brand) ? true : false
    }

    onCheckBrandChange = (_e, selectedIndex) => {
        const newSelectedBrandFilter = this.props.home.selectedBrandFilter.map((item, index) => {
            if (index === selectedIndex) {
                return !item
            }
            return item
        })
        this.props.setStates({ selectedBrandFilter: newSelectedBrandFilter })
    }

    onCheckRAMChange = (_e, selectedIndex) => {
        const newSelectedRAMFilter = this.props.home.selectedRAMFilter.map((item, index) => {
            if (index === selectedIndex) {
                return !item
            }
            return item
        })
        this.props.setStates({ selectedRAMFilter: newSelectedRAMFilter })
    }

    onCheckStorageChange = (_e, selectedIndex) => {
        const newSelectedStorageFilter = this.props.home.selectedStorageFilter.map((item, index) => {
            if (index === selectedIndex) {
                return !item
            }
            return item
        })
        this.props.setStates({ selectedStorageFilter: newSelectedStorageFilter })
    }

    onFromPriceChange = (e) => {
        const checkPosNum = /^[1-9][0-9]*$/
        const value = e.target.value
        if (checkPosNum.test(value) || value === "") {
            this.props.setStates({ fromPrice: e.target.value })
        }
    }

    onToPriceChange = (e) => {
        const checkPosNum = /^[1-9][0-9]*$/
        const value = e.target.value
        if (checkPosNum.test(value) || value === "") {
            this.props.setStates({ toPrice: e.target.value })
        }
    }
    onApplyFilter = () => {
        //call api search

    }

    onRemoveAllFilters = async() => {
        const newFilters = {
            selectedStorageFilter: this.props.home.selectedBrandFilter.map(() => false),
            selectedBrandFilter: this.props.home.selectedBrandFilter.map(() => false),
            selectedRAMFilter: this.props.home.selectedRAMFilter.map(() => false),
            fromPrice: "",
            toPrice: "",
            searchString: "",
        }

        //call API to get item
        const currentPage = 1
        const pageSize = 10
        const items = await Api.getItems(currentPage, pageSize)

        //set state redux 
        const data = {...newFilters, ...items}
        this.props.setStates(data)
    }

    onHandleClickItem = (item) => {
        this.props.navigate(`/${item.id}`)
    }

    onSearchItems = async() => {
        //call api search
        const currentPage = 1
        const pageSize = 10
        const searchItems = await Api.getItems(currentPage, this.props.home.searchString, pageSize)

        this.props.setStates(searchItems)
    }

    onSearchStringChange = (e) => {
        this.props.setStates({
            searchString: e.target.value
        })
        if (e.key === 'Enter' || e.keyCode === 13) {
            //call api wwhen press enter 
            this.onSearchItems()
            return
        }
    }

    render() {
        return (
            <div className="home">
                <Header />
                <div className="home-content">
                    <div className="filter-list">
                        <div className="search">
                            <div className="filters-text">
                                Tìm kiếm
                            </div>

                            <TextField
                                variant="outlined"
                                size='small'
                                placeholder='Tìm kiếm sản phẩm'
                                value={this.props.home.searchString}
                                onChange={this.onSearchStringChange}
                                onKeyDown={this.onSearchStringChange}
                                InputProps={{
                                    startAdornment: (
                                        <Button
                                            endIcon={<SearchIcon />}
                                            onClick={this.onSearchItems}
                                        />
                                    )
                                }}
                            />
                        </div>
                        <div className="brand-filters">
                            <div className="filters-text">
                                Hãng sản xuất
                            </div>
                            <div className="brands">
                                {this.props.home.brandFilters.map((brand, index) => {
                                    const isChecked = this.props.home.selectedBrandFilter[index]
                                    return (
                                        <div className="brand-filter" key={index}>
                                            <FormControlLabel
                                                label={brand}
                                                control={
                                                    <Checkbox
                                                        icon={<CircleUnchecked />}
                                                        checkedIcon={<CircleCheckedFilled />}
                                                        checked={isChecked}
                                                        onChange={(e) => this.onCheckBrandChange(e, index)}
                                                    />
                                                }
                                            />
                                        </div>
                                    )
                                })}
                            </div>
                        </div>

                        <div className="price-filters">
                            <div className="filters-text">
                                Mức giá
                            </div>
                            <div className="filter">
                                <div className="gap">
                                    Từ
                                </div>
                                <div className="from-price">
                                    <TextField
                                        value={this.props.home.fromPrice}
                                        onChange={(e) => this.onFromPriceChange(e)}
                                        size="small"
                                    />
                                </div>
                                <div className="gap">
                                    đến
                                </div>
                                <div className="to-price">
                                    <TextField
                                        value={this.props.home.toPrice}
                                        onChange={(e) => this.onToPriceChange(e)}
                                        size="small"
                                    />
                                </div>
                            </div>
                        </div>

                        <div className="ram-filters">
                            <div className="filters-text">
                                RAM
                            </div>
                            <div className="rams">
                                {this.props.home.RAMFilters.map((ram, index) => {
                                    const isChecked = this.props.home.selectedRAMFilter[index]
                                    return (
                                        <div className="ram-filter" key={index}>
                                            <FormControlLabel
                                                label={ram}
                                                control={
                                                    <Checkbox
                                                        icon={<CircleUnchecked />}
                                                        checkedIcon={<CircleCheckedFilled />}
                                                        checked={isChecked}
                                                        onChange={(e) => this.onCheckRAMChange(e, index)}
                                                    />
                                                }
                                            />
                                        </div>
                                    )
                                })}
                            </div>
                        </div>

                        <div className="storage-filters">
                            <div className="filters-text">
                                Ổ cứng
                            </div>
                            <div className="storages">
                                {this.props.home.storageFilters.map((storage, index) => {
                                    const isChecked = this.props.home.selectedStorageFilter[index]
                                    return (
                                        <div className="storage-filter" key={index}>
                                            <FormControlLabel
                                                label={storage}
                                                control={
                                                    <Checkbox
                                                        icon={<CircleUnchecked />}
                                                        checkedIcon={<CircleCheckedFilled />}
                                                        checked={isChecked}
                                                        onChange={(e) => this.onCheckStorageChange(e, index)}
                                                    />
                                                }
                                            />
                                        </div>
                                    )
                                })}
                            </div>
                        </div>
                        <div className="apply-button">
                            <Button variant="text" onClick={() => this.onRemoveAllFilters()}>
                                Hủy bỏ
                            </Button>
                            <div className='gap' />
                            <Button variant="contained" onClick={() => this.onApplyFilter()}>
                                Áp dụng
                            </Button>
                        </div>
                    </div>
                    <div className="product-list">
                        {this.props.home.items.map((item, index) => {
                            return (
                                <Card
                                    key={index}
                                    item={item}
                                    onShowInfo={() => this.onHandleClickItem(item)}
                                />
                            )
                        })}
                    </div>
                </div>
                <div className="pagination">
                    <Pagination
                        count={this.props.home.totalPage}
                        page={this.props.home.currentPage}
                        color="primary"
                        onChange={(_e, value) => this.props.setStates({
                            currentPage: value
                        })}
                    />
                </div>
            </div>
        )
    }
}
const mapStateToProps = (state) => {
    return {
        home: state.home
    }
}

const mapDispatchToProps = (dispatch, _props) => {
    return {
        setStates: (data) => {
            dispatch(action.setStates(data))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(withRouter(Home))
