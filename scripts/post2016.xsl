<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.tei-c.org/ns/1.0">
    <xsl:output method="xml" indent="yes"/>
    <xsl:strip-space elements="*"/>

    <xsl:variable name="fileName" select="replace(document-uri(/),'.*/(.*)\.xml','$1')"/>

    <xsl:template name="root" match='/'>
        <TEI xml:lang="nob" xml:id="{$fileName}" ana="#parla.sitting #reference">
            <xsl:call-template name="teiHeader"/>
            <xsl:call-template name="body"/>
        </TEI>
    </xsl:template>

    <xsl:template name="body">
        <text ana="#reference">
            <body>
                <div type="debateSection">
                    <xsl:apply-templates select="/Forhandlinger/Mote/Startseksjon"/>
                </div>
                <xsl:for-each select="/Forhandlinger/Mote/node()[self::Hovedseksjon]/Saker/node()[self::*]">
                    <div type="debateSection">
                        <head>
                            <xsl:value-of select="Sakshode/Saknr/normalize-space()"/>
                            <xsl:text> </xsl:text>
                            <xsl:value-of select="Sakshode/Saktittel/normalize-space()"/>
                        </head>
                        <xsl:apply-templates/>
                    </div>
                </xsl:for-each>
                <div type="debateSection">
                    <xsl:apply-templates select="/Forhandlinger/Mote/Sluttseksjon"/>
                </div>
            </body>
        </text>
    </xsl:template>

    <xsl:template name="presidentinnlegg" match="Presinnlegg">
        <xsl:variable name="president_navn" select="preceding::node()[self::Merknad[contains(., 'presidentplass')]/normalize-space() or self::President][1]//Uth/normalize-space()"/>
        <note type="speaker"
            xmlns="http://www.tei-c.org/ns/1.0">
            <xsl:value-of select='A/Navn/normalize-space()'/>
        </note>
        <xsl:call-template name="u_tag">
            <xsl:with-param name="speaker_name" select="$president_navn"></xsl:with-param>
            <xsl:with-param name="speaker_type">#chair</xsl:with-param>
        </xsl:call-template>
    </xsl:template>

    <xsl:template name="innlegg" match='node()[self::Hovedinnlegg or self::Replikk]'>
        
        <xsl:param name="speaker_id" select="A/Navn/@personID"/>
          
        <xsl:choose>
            <!-- The following when statement deals with cases where one element of speech have multiple speakers, most likely because of errors in the transcription -->
            <xsl:when test="count(A/Navn) > 1">
                <xsl:for-each-group select="*" group-starting-with="*[child::Navn]">
                    <note type="speaker">
                        <xsl:value-of select="Navn/normalize-space()"/>
                    </note>
                    <u who="{Navn/@personID/normalize-space()}" name="{substring-before(Navn[1], ' [')}" ana="#regular"
                       xml:id="{$fileName}.u{generate-id(.)}">
                        <xsl:for-each select="current-group()">
                            <xsl:call-template name="segment"/>
                        </xsl:for-each>
                    </u>
                    <xsl:text>

                    </xsl:text>
                </xsl:for-each-group>
            </xsl:when>

            <xsl:otherwise>
                <xsl:variable name="speaker_name" select="substring-before(A/Navn/normalize-space(), ' [')"/>
                <note type="speaker"
                    xmlns="http://www.tei-c.org/ns/1.0">
                    <xsl:value-of select='A/Navn/normalize-space()'/>
                </note>
                <xsl:call-template name="u_tag">
                    <xsl:with-param name="speaker_id" select="$speaker_id"/>
                    <xsl:with-param name="speaker_name" select="$speaker_name"/>
                    <xsl:with-param name="speaker_type">#regular</xsl:with-param>
                </xsl:call-template>
            </xsl:otherwise>
            </xsl:choose>


        </xsl:template>

    <xsl:template name="u_tag">
        <xsl:param name="speaker_id"/>
        <xsl:param name="speaker_name"/>
        <xsl:param name="speaker_type"/>       

        <u who="{$speaker_id}" name="{$speaker_name}" ana="{$speaker_type}"
          xml:id="{$fileName}.u{generate-id(.)}">
            <xsl:for-each select="descendant::A">
                <xsl:call-template name="segment"/>
            </xsl:for-each>
        </u>
    </xsl:template>

    <!-- For speech segments -->
    <xsl:template name="segment">
        <seg xml:id="{$fileName}.seg{generate-id(.)}">
            <xsl:value-of select="node()[not(self::Navn)]/normalize-space()"/>
        </seg>
    </xsl:template>

    <!-- For transciber notes -->
    <xsl:template match="text()">
        <xsl:variable name="grandparent">
            <xsl:value-of select="name(../..)"></xsl:value-of>
        </xsl:variable>
        <note type="{$grandparent}">
            <xsl:value-of select="normalize-space()"/>
        </note>
    </xsl:template>

    <xsl:template match='node()[not(self::text() or self::Hovedinnlegg or self::Replikk or self::Presinnlegg)]'>
        <xsl:apply-templates/>
    </xsl:template>

    <!-- Debate topic. Processed elsewhere so needs to be empty -->
    <xsl:template match="Sakshode">
    </xsl:template>


    <xsl:template name="teiHeader">
        <teiHeader>
            <date>
                <xsl:value-of select="$fileName"/>
            </date>
            <fileDesc>
                <titleStmt>
                    <title type="main" xml:lang="nob">The Norwegian parliamentary corpus ParlaMint-NO, Session XXXX, Sitting XXX [ParlaMint]</title>
                    <title type="main" xml:lang="en">Hansard of the session of the Norwegian Parliament (Stortinget), 20141, M51 (2015-02-03), final version</title>
                    <title type='sub' xml:lang="nob">PLACEHOLDER</title>
                    <title type='sub' xml:lang="en">PLACEHOLDER</title>   
                    <meeting ana="#parla.session">20141</meeting>
                    <respStmt>
                        <persName>Lars Magne Tungland</persName>
                        <resp xml:lang="en">Data retrieval and conversion to TEI</resp>
                    </respStmt>
                    <funder>
                        <orgName xml:lang="en">The CLARIN research infrastructure</orgName>
                    </funder>
                    <funder>
                        <orgName xml:lang="en">European Commission</orgName>
                    </funder>
                    <funder>
                        <orgName xml:lang="en">National Library of Norway</orgName>
                    </funder>
                </titleStmt>
                <editionStmt>
                    <edition>0.1</edition>
                </editionStmt>
                <extent>
                    
                </extent>
                <publicationStmt>
                    <publisher>
                        <orgName xml:lang="en">The CLARIN research infrastructure</orgName>
                        <ref target="https://www.clarin.eu/">www.clarin.eu</ref>
                    </publisher>
                    <idno subtype="handle" type="URI">http://hdl.handle.net/11356/1432</idno>
                    <availability status="free">
                        <licence>http://creativecommons.org/licenses/by/4.0/</licence>
                        <p xml:lang="en">
            This work is licensed under the
                            <ref target="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</ref>
            .
                        </p>
                    </availability>
                    <date when="2021-06-07">June 7, 2021</date>
                </publicationStmt>
                <sourceDesc>
                    <bibl>
                        <title type="main" xml:lang="en">Hansards of the Norwegian Parliament</title>
                        <publisher xml:lang="en">The Norwegian Parliament</publisher>
                        <idno type="URI">https://www.stortinget.no/</idno>
                        <date when="2015-02-03">2015-02-03</date>
                    </bibl>
                </sourceDesc>
            </fileDesc>
            <encodingDesc>
                <projectDesc>
                    <p xml:lang="en">
                        <ref target="https://www.clarin.eu/content/parlamint">ParlaMint</ref>
                    </p>
                </projectDesc>
                <tagsDecl>
                
                </tagsDecl>
            </encodingDesc>
            <profileDesc>
                <settingDesc>
                    <setting>
                        <name type="address">Karl Johans Gate 22</name>
                        <name type="city">0026 Oslo</name>
                        <name type="country" key="NO">Norway</name>
                        <date ana="#parla.sitting" when="2015-02-03">2015-02-03</date>
                    </setting>
                </settingDesc>
            </profileDesc>
            <revisionDesc xml:lang="en">
                <change when="2021-01-29">
                    <name>Lars Magne Tungland</name>
            : Generated corpus in ParlaMint.
                </change>
            </revisionDesc>
        </teiHeader>
    </xsl:template>



</xsl:stylesheet>