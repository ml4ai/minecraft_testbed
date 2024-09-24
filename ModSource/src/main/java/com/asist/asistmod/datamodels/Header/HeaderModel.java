package com.asist.asistmod.datamodels.Header;

import java.time.Clock;

public class HeaderModel {
	
	public String timestamp = Clock.systemUTC().instant().toString();
	
	public String message_type = null;
	
	public String version = "1.1";

}
