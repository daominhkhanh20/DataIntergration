import React, { Component } from 'react'
import Image from '../../icon'
import './index.scss'

export default class Card extends Component {
    constructor(props) {
        super(props)
        this.state = {

        }
    }

    componentDidMount() {

    }

    onHandleClick = () => {
        this.props.onShowInfo()
    }

    render() {
        return (
            <div className={"product-info-card"} onClick = {() => this.onHandleClick()}>
                <div className="name">
                    {this.props.item.name}
                </div>
                <div className="price">
                    {this.props.item.price.toLocaleString('it-IT', {style : 'currency', currency : 'VND'})}
                </div>
                <div className="info">
                    <img src = {Image.monitor} alt = ""/>
                    <div className="name">
                        {this.props.item.brand}
                    </div>
                </div>
                <div className="info">
                    <img src = {Image.CPU} alt = ""/>
                    <div className="name">
                        {this.props.item.CPU}
                    </div>
                </div>
                <div className="info">
                    <img src = {Image.GPU} alt = ""/>
                    <div className="name">
                        {this.props.item.GPU}
                    </div>
                </div>
                <div className="info">
                    <img src = {Image.RAM} alt = ""/>
                    <div className="name">
                        {this.props.item.RAM}
                    </div>
                </div>
                <div className="info">
                    <img src = {Image.storage} alt = ""/>
                    <div className="name">
                        {this.props.item.storage}
                    </div>
                </div>
                <div className="info">
                    <img src = {Image.shop} alt = ""/>
                    <div className="name">
                        {this.props.item.shopNum}
                    </div>
                </div>
            </div>
        )
    }
}
