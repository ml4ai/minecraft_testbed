package com.asist.asistmod.block;

import java.util.Random;

import net.minecraft.block.state.IBlockState;
import net.minecraft.util.EnumParticleTypes;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

public class BlockVictim_2 extends BlockVictimBase {
	
	public BlockVictim_2() {
		this.setHardness(2f);	
	}
	
	@SideOnly(Side.CLIENT)
	@Override
    public void randomDisplayTick(IBlockState stateIn, World worldIn, BlockPos pos, Random rand)
    {	 		
	 		double d0 = (double)((float)pos.getX() + 0.4F + rand.nextFloat() * 0.2F);
	        double d1 = (double)((float)pos.getY() + 0.7F + rand.nextFloat() * 0.3F);
	        double d2 = (double)((float)pos.getZ() + 0.4F + rand.nextFloat() * 0.2F);
	        worldIn.spawnParticle(EnumParticleTypes.SPELL, d0, d1, d2, 0.0D, 1.0D, 0.0D, new int[0]);
	        
	        d0 = (double)((float)pos.getX() + 0.4F + rand.nextFloat() * 0.2F);
	        d1 = (double)((float)pos.getY() + 0.7F + rand.nextFloat() * 0.3F);
	        d2 = (double)((float)pos.getZ() + 0.4F + rand.nextFloat() * 0.2F);
	        worldIn.spawnParticle(EnumParticleTypes.SPELL, d0, d1, d2, 0.0D, 1.0D, 0.0D, new int[0]);
	        
    }
	
}
