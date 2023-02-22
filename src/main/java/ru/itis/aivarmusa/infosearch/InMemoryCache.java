package ru.itis.aivarmusa.infosearch;

import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;


@Service
public class InMemoryCache {

    private final Map<String, Object> map = new ConcurrentHashMap<>();

    public Object put(String key, Object value) {
        return map.put(key, value);
    }

    public Object get(String key) {
        return get(key, null);
    }

    public Object get(String key, Object defValue) {
        return map.computeIfAbsent(key, key1 -> defValue);
    }

}
