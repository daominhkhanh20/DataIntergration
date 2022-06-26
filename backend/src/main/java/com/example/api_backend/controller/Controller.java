/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.example.api_backend.controller;

import com.example.api_backend.repository.ItemRepository;
import com.example.api_backend.repository.dao.Item;
import com.example.api_backend.repository.dao.Product;

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
    public List<Item> paginate(Integer page) {
        if (page == null) {
            page = 1;
        }
        if (page < 1) {
            return null;
        }
        Pageable pageable = PageRequest.of(page - 1, 10);
        Page<Item> p = itemRepo.findAll(pageable);

        return p.getContent();
    }

    @GetMapping("/find")
    public List<Item> findByKeyword(@RequestParam("keyword") String keyword) {
        List<Item> items = itemRepo.findByKeyword(".*" + keyword + ".*");
        return items;
    }

    @GetMapping("/show/item")
    public Item findItemByID(@RequestParam("id") ObjectId id) {
        Item item = itemRepo.findByID(id);
        System.out.println(id);
        return item;
    }

    @GetMapping("/show/product")
    public Product findProductByID(@RequestParam("itemId") String itemId, @RequestParam("productId") String productId) {
        Item item = itemRepo.findByID(new ObjectId(itemId));
        List<Product> products = item.getInformation();
        for (Product p : products) {
            if (p.getId().equals(productId)) {
                return p;
            }

        }
        return null;
    }

}
