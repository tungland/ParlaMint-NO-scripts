<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.tei-c.org/ns/1.0"
   
    >
    <xsl:output method="xml" indent="yes"/>

    <xsl:variable name="filename" select="replace(document-uri(/),'.*/(.*)\.xml','$1')"/>



<xsl:template match='node()|@*'>

    <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
</xsl:template>

<!-- <xsl:template match='*:s'>
    <s xml:id="{$filename}.s{generate-id(.)}">
        
            <xsl:apply-templates select="@*|node()"/>
        
    </s>
</xsl:template>

<xsl:template match='*:w'>
    <w xml:id="{$filename}.w{generate-id(.)}">
      
            <xsl:apply-templates select="@*|node()"/>
      
    </w>
</xsl:template> -->


</xsl:stylesheet>