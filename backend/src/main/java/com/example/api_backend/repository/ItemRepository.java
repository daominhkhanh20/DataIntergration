/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.example.api_backend.repository;

import com.example.api_backend.repository.dao.ItemEntity;
import com.example.api_backend.repository.dao.Product;
import java.util.List;
import org.bson.types.ObjectId;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

/**
 *
 * @author 20183556
 */
public interface ItemRepository extends MongoRepository<ItemEntity, ObjectId> {

    @Override
    public List<ItemEntity> findAll();

    @Query("{'product_name': {$regex: ?0 }})")
    //public List<Item> findByKeyword(String keyword);
    public Page<ItemEntity> findByKeyword(String keyword, Pageable pageable);

    @Query("{'product_name': {$regex: ?0 }})")
    public List<ItemEntity> findByKeyword(String keyword);

    @Query("{'_id': ?0}")
    public ItemEntity findByID(ObjectId id);

    @Query("{'count': {$gt: ?0 }})")
    public List<ItemEntity> findByCondition(Integer count);

    @Override
    public long count();

}
