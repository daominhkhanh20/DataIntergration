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
import java.util.stream.Collectors;
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
        Pageable pageable = PageRequest.of(page - 1, 8);
//        List<ItemEntity> it = itemRepo.findAll();
        long size = itemRepo.count();
        System.out.println(size);
        int totalPage;
        if (size % 8 == 0) {
            totalPage = (int) (size / 8);
        } else {
            totalPage = (int) (size / 8 + 1);
        }
        Page<ItemEntity> p = itemRepo.findAll(pageable);
        List<ItemEntity> itemEntitys = p.getContent();
        List<ItemResponse> items = new ArrayList<>();
        itemEntitys.forEach(item -> {
            items.add(ItemResponse.builder()
                    .id(item.getId().toHexString())
                    .name(item.getName())
                    .information(item.getInformation())
                    .totalPage(totalPage)
                    .build());
        });
        return items;
    }

    @GetMapping("/all_matching")
    public List<ItemResponse> getItemMatching(Integer page) {
        if (page == null) {
            page = 1;
        }
        if (page < 1) {
            return null;
        }
        List<ItemEntity> it = itemRepo.findByCondition(1);
        System.out.println(it.size());
        int totalPage;
        if (it.size() % 8 == 0) {
            totalPage = it.size()/8;

        } else {
            totalPage = it.size()/8 + 1;
        }
        List<ItemEntity> Listitem = it.stream().skip(8 * (page - 1)).limit(8).collect(Collectors.toList());
        List<ItemResponse> items = new ArrayList<>();
        Listitem.forEach(item -> {
            items.add(ItemResponse.builder()
                    .id(item.getId().toHexString())
                    .name(item.getName())
                    .information(item.getInformation())
                    .totalPage(totalPage)
                    .build());
        });
        return items;
    }

    @GetMapping("/find")
    public List<ItemResponse> findByKeyword(@RequestParam("keyword") String keyword, Integer page) {
        if (page == null) {
            page = 1;
        }
        if (page < 1) {
            return null;
        }
        int totalPage;
        List<ItemEntity> tmp = itemRepo.findByKeyword(".*" + keyword + ".*");
        if (tmp.size() % 8 == 0) {
            totalPage = tmp.size()/8;
        } else {
            totalPage = tmp.size()/8 + 1;
        }
        List<ItemEntity> Listitem = tmp.stream().skip(8 * (page - 1)).limit(8).collect(Collectors.toList());
        List<ItemResponse> items = new ArrayList<>();
        Listitem.forEach(item -> {
            items.add(ItemResponse.builder()
                    .id(item.getId().toHexString())
                    .name(item.getName())
                    .information(item.getInformation())
                    .totalPage(totalPage)
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
