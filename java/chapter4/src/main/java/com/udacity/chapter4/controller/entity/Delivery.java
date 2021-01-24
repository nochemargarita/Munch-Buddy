package com.udacity.chapter4.controller.entity;

import org.hibernate.annotations.Nationalized;
import org.hibernate.annotations.Type;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
public class Delivery {
    @Id
    @GeneratedValue
    Long id;

    @Nationalized
    private String name;
    @Column(name = "address_full", length = 500)
    private String address;
    private LocalDateTime deliveryTime;
    @Type(type = "yes_no")
    private Boolean completed

    public Delivery() {
    }

    public Delivery(Long id, String name, String address, LocalDateTime deliveryTime, Boolean completed) {
        this.id = id;
        this.name = name;
        this.address = address;
        this.deliveryTime = deliveryTime;
        this.completed = completed;
    }

    public Delivery(String name, String address, LocalDateTime deliveryTime, Boolean completed) {
        this.name = name;
        this.address = address;
        this.deliveryTime = deliveryTime;
        this.completed = completed;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public LocalDateTime getDeliveryTime() {
        return deliveryTime;
    }

    public void setDeliveryTime(LocalDateTime deliveryTime) {
        this.deliveryTime = deliveryTime;
    }

    public Boolean getCompleted() {
        return completed;
    }

    public void setCompleted(Boolean completed) {
        this.completed = completed;
    }
}
