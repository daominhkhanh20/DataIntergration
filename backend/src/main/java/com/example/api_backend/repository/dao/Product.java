/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.example.api_backend.repository.dao;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

/**
 *
 * @author 20183556
 */
@Document("data_matching2v1")
@Data
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Product {
    @Id
    @Field(value = "_id")
    private String id;
    
    @Field(value = "Hệ điều hành")
    private String os;
    
    @Field(value = "web")
    private String web;
    
    @Field(value = "Bộ vi xử lý")
    private String cpu;
    
    
    @Field(value = "Hãng sản xuất")
    private String brand;
    
    @Field(value = "Webcam")
    private String webcam;
    
    @Field(value = "image_url")
    private String image_url;
    
    @Field(value = "Pin")
    private String pin;
    
    @Field(value = "product_name")
    private String product_name;
    
    @Field(value = "Cân nặng")
    private String weight;
    
    @Field(value = "VGA")
    private String VGA;
    
    @Field(value = "price")
    private String price;
    
    @Field(value = "product_url")
    private String product_url;
    
    @Field(value = "device")
    private String device;
    
    @Field(value = "Card Reader")
    private String card_reader;
    
    @Field(value = "Kích thước (rộng x dài x cao)")
    private String dimension;
    
    @Field(value = "Bộ nhớ trong")
    private String rom;
    
    @Field(value = "Ổ cứng")
    private String disk;
    
    @Field(value = "Màn hình")
    private String monitor;
    
    
    @Field(value = "Giao tiếp không dây")
    private String wireless;
    
    @Field(value = "Cổng giao tiếp")
    private String connection_port;
    
    @Field(value = "Chủng loại")
    private String model;
   
    
    @Field(value = "Mầu sắc")
    private String color;
    
}
