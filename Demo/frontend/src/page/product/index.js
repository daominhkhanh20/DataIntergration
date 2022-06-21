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
class Product extends Component {
    constructor(props) {
        super(props)
        this.state = {
            name: "Laptop Acer TravelMate B3 TMB311 31 P49D N5030/4GB/256GB/Win11 (NX.VNFSV.005)  ",
            imageUrl: "https://laptopworld.vn/media/product/9983_lenovo_thinkpad_e15_gen_2_4.jpg",
            CPU: "PentiumN50301.1GHz",
            RAM: 8,
            storage: 256,
            card: "Card tích hợp Intel UHD 605",
            brand: "Acer ",
            stores: [
                {
                    name: "tgdd",
                    url: "https://www.thegioididong.com/laptop/acer-travelmate-b3-tmb311-31-p49d-n5030-nxvnfsv005?src=osp",
                    price: 1000000000,
                    OS: "Window 11",
                    screen: '11.6"HD (1366 x 768)',
                    battery: "57 Wh",
                    weight: "2.3 kg",
                    color: "Gray",
                    material: "Gray"
                },
                {
                    name: "tgdd1",
                    url: "https://www.thegioididong.com/laptop/acer-travelmate-b3-tmb311-31-p49d-n5030-nxvnfsv005?src=osp",
                    price: 1000000000,
                    OS: "Window 11",
                    screen: '11.6"HD (1366 x 768)',
                    battery: "57 Wh",
                    weight: "2.3 kg",
                    color: "Gray",
                    material: "Gray"
                }
            ]
        }
    }

    componentDidMount() {

    }

    onHandleClickBack() {
        this.props.navigate("/")
    }

    render() {
        return (
            <div className='product-detail'>
                <Header />
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
                        <span>{this.state.name}</span>
                    </div>
                    <div className='detail'>
                        <img src={this.state.imageUrl} alt="" />
                        <div className='basic-details'>
                            <div className='basic-detail'>
                                <div className='key'>CPU:</div>
                                <div className='value'>{this.state.CPU}</div>
                            </div>
                            <div className='basic-detail'>
                                <div className='key'>RAM:</div>
                                <div className='value'>{this.state.RAM} GB</div>
                            </div>
                            <div className='basic-detail'>
                                <div className='key'>Storage:</div>
                                <div className='value'>{this.state.storage} GB</div>
                            </div>
                            <div className='basic-detail'>
                                <div className='key'>Card:</div>
                                <div className='value'>{this.state.card}</div>
                            </div>
                            <div className='basic-detail'>
                                <div className='key'>Brand:</div>
                                <div className='value'>{this.state.brand}</div>
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
                                    <TableCell align="left">Material</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {this.state.stores.map((store) => (
                                    <TableRow
                                        key={store.name}
                                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                    >
                                        <TableCell align='left'>
                                            <a href={store.url}>
                                                {store.name}
                                            </a>
                                        </TableCell>
                                        <TableCell align="left">{store.price.toLocaleString('it-IT', { style: 'currency', currency: 'VND' })}</TableCell>
                                        <TableCell align="left">{store.OS}</TableCell>
                                        <TableCell align="left">{store.screen}</TableCell>
                                        <TableCell align="left">{store.battery}</TableCell>
                                        <TableCell align="left">{store.weight}</TableCell>
                                        <TableCell align="left">{store.color}</TableCell>
                                        <TableCell align="left">{store.material}</TableCell>
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
