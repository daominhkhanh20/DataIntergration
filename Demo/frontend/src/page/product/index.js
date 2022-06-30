import React, { Component } from 'react'
import Header from '../../component/header'
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import './index.scss'
import { Button } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { withRouter } from '../../util/withRouter';
import Api from '../../api/api';
import LoadingScreen from '../../component/loading';
class Product extends Component {
    constructor(props) {
        super(props)
        this.state = {
            name: "",
            imageUrl: "",
            CPU: "",
            RAM: "",
            storage: "",
            GPU: "",
            brand: " ",
            stores: [],
            loading: true
        }
    }

    mapAPIToState = (item) => {
        return (
            {
                name: item.name,
                brand: item.information.find((item) => item.brand !== "NaN")?.brand || "Unknown",
                CPU: item.information.find((item) => item.cpu !== "NaN")?.cpu || "Unknown",
                GPU: item.information.find((item) => item.vga !== "NaN")?.vga || "Unknown",
                RAM: item.information.find((item) => item.rom !== "NaN")?.rom || "Unknown",
                storage: item.information.find((item) => item.disk !== "NaN")?.disk || "Unknown",
                imageUrl: item.information.find((item) => item.image_url !== "NaN")?.image_url || "Unknown",
                stores: item.information.map((info) => ({
                    name: info.web,
                    url: info.product_url,
                    price: Number(info.price),
                    OS: info.os === "NaN" ? "Unknown" : this.capitalizeFirstLetter(info.os),
                    screen: info.monitor === "NaN" ? "Unknown" : this.capitalizeFirstLetter(info.monitor),
                    battery: info.pin === "NaN" ? "Unknown" : this.capitalizeFirstLetter(info.pin),
                    color: info.color === "NaN" ? "Unknown" : this.capitalizeFirstLetter(info.color),
                    dimension: info.dimension === "NaN" ? "Unknown" : this.capitalizeFirstLetter(info.dimension),
                    weight: info.weight === "NaN" ? "Unknown" : this.capitalizeFirstLetter(info.weight),
                }))
            }
        )
    }

    capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    componentDidMount = async () => {
        const id = this.props.params.id
        this.setState({
            loading: true
        })

        const res = await Api.getItem(id)
        const item = this.mapAPIToState(res.data)
        this.setState({
            ...item,
            loading: false
        })
    }

    onHandleClickBack() {
        this.props.navigate("/")
    }

    render() {
        return (
            <div className='product-detail'>
                <Header />
                <LoadingScreen open={this.state.loading} />
                <div className='back'>
                    <Button
                        startIcon={<ArrowBackIcon />}
                        onClick={() => this.onHandleClickBack()}
                    >
                        Về trang chủ
                    </Button>
                </div>
                <div className='info'>
                    <div className='name'>
                        <span>{this.state.name.toUpperCase()}</span>
                    </div>
                    <div className='detail'>
                        <img src={this.state.imageUrl} alt="" />
                        <div className='basic-details'>
                            <div className='basic-detail'>
                                <div className='key'>CPU:</div>
                                <div className='value'>{this.capitalizeFirstLetter(this.state.CPU)}</div>
                            </div>
                            <div className='basic-detail'>
                                <div className='key'>RAM:</div>
                                <div className='value'>{this.capitalizeFirstLetter(this.state.RAM)}</div>
                            </div>
                            <div className='basic-detail'>
                                <div className='key'>Storage:</div>
                                <div className='value'>{this.capitalizeFirstLetter(this.state.storage)}</div>
                            </div>
                            <div className='basic-detail'>
                                <div className='key'>Card:</div>
                                <div className='value'>{this.capitalizeFirstLetter(this.state.GPU)}</div>
                            </div>
                            <div className='basic-detail'>
                                <div className='key'>Brand:</div>
                                <div className='value'>{this.state.brand.toUpperCase()}</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className='store-details'>
                    <div className='text'>
                        Danh các cửa hàng
                    </div>
                    <TableContainer component={Paper}>
                        <Table sx={{ minWidth: 650 }} aria-label="simple table">
                            <TableHead>
                                <TableRow>
                                    <TableCell align="left">Store</TableCell>
                                    <TableCell align="left">Price</TableCell>
                                    <TableCell align="left">OS</TableCell>
                                    <TableCell align="left">Screen</TableCell>
                                    <TableCell align="left">Battery</TableCell>
                                    <TableCell align="left">Weight</TableCell>
                                    <TableCell align="left">Color</TableCell>
                                    <TableCell align="left">Dimension</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {this.state.stores.map((store) => (
                                    <TableRow
                                        key={store.url}
                                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                    >
                                        <TableCell align='left'>
                                            <a href={store.url} target="_blank" rel="noopener noreferrer">
                                                {store.name}
                                            </a>
                                        </TableCell>
                                        <TableCell align="left">{store.price.toLocaleString('it-IT', { style: 'currency', currency: 'VND' })}</TableCell>
                                        <TableCell align="left">{store.OS}</TableCell>
                                        <TableCell align="left">{store.screen}</TableCell>
                                        <TableCell align="left">{store.battery}</TableCell>
                                        <TableCell align="left">{store.weight}</TableCell>
                                        <TableCell align="left">{store.color}</TableCell>
                                        <TableCell align="left">{store.dimension}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </div>
            </div>
        )
    }
}
export default withRouter(Product)
