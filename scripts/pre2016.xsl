<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="yes"/>
    <xsl:strip-space elements="*"/>

    <xsl:variable name="fileName" select="replace(document-uri(/),'.*/(.*)\.xml','$1')"/>


    <xsl:template match="/">
        <TEI xmlns="http://www.tei-c.org/ns/1.0" xml:lang="nob" xml:id="{$fileName}" ana="#parla.sitting #reference">
            <teiHeader>
                <date>
                    <xsl:value-of select="$fileName"/>
                </date>
                <fileDesc>
                    <titleStmt>
                        <title type="main" xml:lang="nob">Norwegian parliamentary corpus ParlaMint-NO, Session XXXX, Sitting XXX [ParlaMint]</title>
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
                        <namespace name="http://www.tei-c.org/ns/1.0">
                       
                        </namespace>
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
            <text ana="#reference">
            <body>
                <xsl:for-each select="forhandling/mote/*">
                    <div type="debateSection">
                        <head>
                            <!-- <xsl:value-of select="node()[sak/sakshode/* | dato]/normalize-space()" separator=" "/> -->
                            <!-- <xsl:value-of select="node()[sak/sakshode/self::tit or self::dato]/normalize-space()" separator=" "/> -->
                            <xsl:value-of select="dato/normalize-space()"/>
                            <xsl:value-of select="sak/sakshode/tit/normalize-space()"/>
                        </head>
                        <xsl:apply-templates/>
                    </div>
                </xsl:for-each>
            </body>
        </text>
        </TEI>
    </xsl:template>

    <xsl:template match="presinnl">
        <!-- Template for meeting president utterances.  -->
        <xsl:variable name="presname" select="preceding::node()[self::uth/ancestor::handling[contains(., 'presidentplass')] or self::president][1]/normalize-space(replace(., 'President: ', ''))"></xsl:variable>
        <!-- <note type="speaker" xmlns="http://www.tei-c.org/ns/1.0">
            <xsl:value-of select="navn"/>
        </note> -->
        <!-- Presidentinnlegg inneholder ikke navnefelt før 2016 -->
        <u who="" name="{$presname}" ana="#chair"
            xmlns="http://www.tei-c.org/ns/1.0" xml:id="{$fileName}.u{generate-id(.)}">
            <xsl:for-each select="node()[not(self::navn)]">
                <xsl:call-template name="seg"/>
            </xsl:for-each>
        </u>
    </xsl:template>

    <xsl:template match="innlegg">
        <xsl:variable name="navn" select="navn/normalize-space(replace(., ':|\[.*\]', ''))"/>
        <note type="speaker"
            xmlns="http://www.tei-c.org/ns/1.0">
            <xsl:value-of select="navn/normalize-space()"/>
        </note>
        <u who="" name="{$navn}" ana="#regular"
            xmlns="http://www.tei-c.org/ns/1.0" xml:id="{$fileName}.u{generate-id(.)}">
            <xsl:for-each select="node()[not(self::navn)]">
                <xsl:call-template name="seg"/>
            </xsl:for-each>
        </u>

    </xsl:template>

    <xsl:template name="seg">
        <seg xmlns="http://www.tei-c.org/ns/1.0" xml:id="{$fileName}.seg{generate-id(.)}">
            <xsl:value-of select="./normalize-space()"/>
        </seg>
    </xsl:template>

    <xsl:template match="text()">
        <note type="{name(..)}"
            xmlns="http://www.tei-c.org/ns/1.0">
            <xsl:value-of select="./normalize-space()"/>
        </note>
    </xsl:template>

    <xsl:template match="sak/sakshode/tit"/>

    <xsl:template match="dato"/>

</xsl:stylesheet>