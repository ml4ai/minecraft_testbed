package com.asist.asistmod.proxy;

import java.io.IOException;

import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.fml.common.FMLLog;
import net.minecraftforge.fml.common.Mod.EventHandler;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPostInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;

public class ServerProxy extends CommonProxy {
	
	
    public void preInit(FMLPreInitializationEvent e) {
    	
    	super.preInit(e);
    	
    	System.out.println( " Hello from server initialization!");
    	System.out.println( " Setting writable permission on maps!");
    	FMLLog.log.info( "Working Directory = " + System.getProperty("user.dir") );
    	
    	String[] cmd = new String[]{"/bin/sh", "chmod 777 -R ."};
    	
    	try {
			Process pr = Runtime.getRuntime().exec(cmd);
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
    }
	
	
    public void init(FMLInitializationEvent e) {
    	super.init(e);    	
    }
	
	
    public void postInit(FMLPostInitializationEvent e) {
    	super.postInit(e);   	
    	
    }
    
    

}
