/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.example.api_backend.repository;

import com.example.api_backend.repository.dao.Item;
import com.example.api_backend.repository.dao.Product;
import java.util.List;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

/**
 *
 * @author 20183556
 */
public interface ItemRepository extends MongoRepository<Item, ObjectId>{
    @Override
    public List<Item> findAll();
    
     @Query("{'product_name': {$regex: ?0 }})")
    public List<Item> findByKeyword(String keyword);
    
    @Query("{'_id': ?0}")
    public Item findByID(ObjectId id);
    
    
}
