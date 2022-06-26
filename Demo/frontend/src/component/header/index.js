import React, { Component } from 'react'
import Image from '../../icon'
import './index.scss'

export default class Header extends Component {
    render() {
        return (
            <div className="home-header">
                <img src={Image.logo} alt={""} />
                <div className="home-header-text">Data Intergration</div>
            </div>
        )
    }
}
