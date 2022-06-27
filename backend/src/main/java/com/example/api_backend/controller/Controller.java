/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.example.api_backend.controller;

import com.example.api_backend.repository.ItemRepository;
import com.example.api_backend.repository.dao.ItemEntity;
import com.example.api_backend.repository.dao.ItemResponse;
import com.example.api_backend.repository.dao.Product;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.ArrayList;
import java.util.Iterator;

import java.util.List;
import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 *
 * @author 20183556
 */
@RestController
public class Controller {

    @Autowired
    ItemRepository itemRepo;

    @GetMapping("/all")
    public List<ItemResponse> paginate(Integer page) {
        if (page == null) {
            page = 1;
        }
        if (page < 1) {
            return null;
        }
        Pageable pageable = PageRequest.of(page - 1, 10);
        Page<ItemEntity> p = itemRepo.findAll(pageable);
        List<ItemEntity> itemEntitys = p.getContent();
        List<ItemResponse> items = new ArrayList<>();
        itemEntitys.forEach(item -> {
            items.add(ItemResponse.builder()
            .id(item.getId().toHexString())
            .name(item.getName())
            .information(item.getInformation())
            .build());
        });
        return items;
    }

    @GetMapping("/find")
    public List<ItemResponse> findByKeyword(@RequestParam("keyword") String keyword,Integer page) {
        if (page == null) {
            page = 1;
        }
        if (page < 1) {
            return null;
        }
        Pageable pageable = PageRequest.of(page - 1, 10);
        Page<ItemEntity> p = itemRepo.findByKeyword(".*" + keyword + ".*",pageable);
        List<ItemEntity> itemEntitys = p.getContent();
        List<ItemResponse> items = new ArrayList<>();
        itemEntitys.forEach(item -> {
            items.add(ItemResponse.builder()
            .id(item.getId().toHexString())
            .name(item.getName())
            .information(item.getInformation())
            .build());
        });
      
        return items;
    }

    @GetMapping("/show/item")
    public ItemEntity findItemByID(@RequestParam("id") ObjectId id) {
        ItemEntity item = itemRepo.findByID(id);
        System.out.println(id);
        return item;
    }

    @GetMapping("/show/product")
    public Product findProductByID(@RequestParam("itemId") String itemId, @RequestParam("productId") String productId) {
        ItemEntity item = itemRepo.findByID(new ObjectId(itemId));
        List<Product> products = item.getInformation();
        for (Product p : products) {
            if (p.getId().equals(productId)) {
                return p;
            }

        }
        return null;
    }

}
